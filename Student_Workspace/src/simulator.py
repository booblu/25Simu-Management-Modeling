"""
Uniswap V3 底层状态机仿真器
实现核心物理行为：池子初始化、同区间交易、跨区间连续吃单
"""

import math
from decimal import Decimal, getcontext
from typing import Dict, Tuple, List

# 设置高精度计算环境
getcontext().prec = 30

# 魔法常数 2^96，用来把普通数字变形成 Q64.96 定点数
Q96 = 2**96

class V3Pool:
    """Uniswap V3 池子状态机"""
    
    def __init__(self, sqrt_price_x96: int, liquidity: int, fee_rate: float = 0.003, 
                 tick_spacing: int = 60, min_tick: int = -887272, max_tick: int = 887272):
        """
        初始化 V3 池子
        
        Args:
            sqrt_price_x96: 初始价格的平方根 (Q64.96格式)
            liquidity: 初始流动性
            fee_rate: 交易费率 (默认0.3%)
            tick_spacing: tick间隔
            min_tick: 最小tick
            max_tick: 最大tick
        """
        self.sqrt_price_x96 = sqrt_price_x96
        self.liquidity = liquidity
        self.fee_rate = fee_rate
        self.tick_spacing = tick_spacing
        self.min_tick = min_tick
        self.max_tick = max_tick
        
        # 状态变量
        self.current_tick = self._sqrt_price_to_tick(sqrt_price_x96)
        self.fee_growth_global = 0
        
        # 跨区间交易记录
        self.crossed_ticks: List[int] = []
        
        # Tick 管理 (支持多区间)
        self.ticks: Dict[int, Dict] = {}
        self._initialize_ticks()
    
    def _initialize_ticks(self):
        """初始化tick数据结构"""
        # 创建多个流动性区间
        current_tick_index = (self.current_tick // self.tick_spacing) * self.tick_spacing
        
        # 在当前tick附近创建3个流动性区间
        for offset in [-self.tick_spacing, 0, self.tick_spacing]:
            tick_index = current_tick_index + offset
            if self.min_tick <= tick_index <= self.max_tick:
                # 每个区间分配部分流动性
                liquidity_share = self.liquidity // 3
                self.ticks[tick_index] = {
                    'liquidity_net': liquidity_share,
                    'liquidity_gross': liquidity_share,
                    'fee_growth_outside': 0
                }
    
    @staticmethod
    def price_to_sqrtpx96(price: float) -> int:
        """
        仅在初始化时调用此函数
        把人类世界直观的价格 P 转化为底层的 uint256 状态变量
        """
        return int(math.sqrt(price) * Q96)
    
    @staticmethod
    def sqrtpx96_to_price(sqrtpx96: int) -> Decimal:
        """
        只在最后收集数据或可视化时使用！
        把天书解释给 CEO 看
        """
        # 正确的价格转换公式: P = (sqrtPriceX96 / Q96)^2
        sqrt_price_decimal = Decimal(sqrtpx96) / Decimal(Q96)
        return sqrt_price_decimal ** 2
    
    def _sqrt_price_to_tick(self, sqrt_price_x96: int) -> int:
        """将sqrtPriceX96转换为tick索引"""
        price = float(self.sqrtpx96_to_price(sqrt_price_x96))
        return int(math.log(price, 1.0001))
    
    def _tick_to_sqrt_price(self, tick: int) -> int:
        """将tick索引转换为sqrtPriceX96"""
        price = 1.0001 ** tick
        return self.price_to_sqrtpx96(price)
    
    def swap_exact_input(self, amount_in: int, zero_for_one: bool) -> Tuple[int, int]:
        """
        执行精确输入交易（支持跨区间）
        
        Args:
            amount_in: 输入代币数量
            zero_for_one: True表示用token0换token1，False表示用token1换token0
            
        Returns:
            (amount_out, fee_amount)
        """
        # 计算手续费
        fee_amount = int(amount_in * self.fee_rate)
        amount_in_after_fee = amount_in - fee_amount
        
        # 更新全局手续费累计
        self.fee_growth_global += fee_amount
        
        # 清空跨区间记录
        self.crossed_ticks.clear()
        
        # 执行交易计算（支持跨区间）
        if zero_for_one:
            amount_out = self._swap_token0_for_token1_with_crossing(amount_in_after_fee)
        else:
            amount_out = self._swap_token1_for_token0_with_crossing(amount_in_after_fee)
        
        return amount_out, fee_amount
    
    def _swap_token0_for_token1_with_crossing(self, amount_in: int) -> int:
        """用token0购买token1（支持跨区间）"""
        remaining_amount = amount_in
        total_amount_out = 0
        
        while remaining_amount > 0:
            # 获取当前区间的流动性
            current_liquidity = self._get_current_liquidity()
            
            if current_liquidity == 0:
                # 流动性枯竭，无法继续交易
                break
            
            # 计算在当前区间能执行的最大交易量
            sqrt_price = self.sqrt_price_x96
            
            # 计算下一个tick边界
            next_tick = self._get_next_initialized_tick(True)  # zero_for_one=True
            next_sqrt_price = self._tick_to_sqrt_price(next_tick)
            
            # 计算在当前区间能消耗的token0数量
            max_amount_in_current_tick = self._compute_max_input_zero_for_one(
                sqrt_price, next_sqrt_price, current_liquidity
            )
            
            # 确定实际交易量
            amount_in_this_tick = min(remaining_amount, max_amount_in_current_tick)
            
            # 执行当前区间交易
            amount_out_this_tick = self._swap_token0_for_token1_single_tick(
                amount_in_this_tick, current_liquidity
            )
            
            total_amount_out += amount_out_this_tick
            remaining_amount -= amount_in_this_tick
            
            # 检查是否需要跨区间
            if remaining_amount > 0 and abs(self.sqrt_price_x96 - next_sqrt_price) < 1:
                # 跨区间
                self._cross_tick(next_tick, True)
                self.crossed_ticks.append(next_tick)
        
        return total_amount_out
    
    def _swap_token1_for_token0_with_crossing(self, amount_in: int) -> int:
        """用token1购买token0（支持跨区间）"""
        remaining_amount = amount_in
        total_amount_out = 0
        
        while remaining_amount > 0:
            # 获取当前区间的流动性
            current_liquidity = self._get_current_liquidity()
            
            if current_liquidity == 0:
                # 流动性枯竭，无法继续交易
                break
            
            # 计算在当前区间能执行的最大交易量
            sqrt_price = self.sqrt_price_x96
            
            # 计算下一个tick边界
            next_tick = self._get_next_initialized_tick(False)  # zero_for_one=False
            next_sqrt_price = self._tick_to_sqrt_price(next_tick)
            
            # 计算在当前区间能消耗的token1数量
            max_amount_in_current_tick = self._compute_max_input_one_for_zero(
                sqrt_price, next_sqrt_price, current_liquidity
            )
            
            # 确定实际交易量
            amount_in_this_tick = min(remaining_amount, max_amount_in_current_tick)
            
            # 执行当前区间交易
            amount_out_this_tick = self._swap_token1_for_token0_single_tick(
                amount_in_this_tick, current_liquidity
            )
            
            total_amount_out += amount_out_this_tick
            remaining_amount -= amount_in_this_tick
            
            # 检查是否需要跨区间
            if remaining_amount > 0 and abs(self.sqrt_price_x96 - next_sqrt_price) < 1:
                # 跨区间
                self._cross_tick(next_tick, False)
                self.crossed_ticks.append(next_tick)
        
        return total_amount_out
    
    def _swap_token0_for_token1_single_tick(self, amount_in: int, liquidity: int) -> int:
        """在单个区间内用token0购买token1"""
        sqrt_price = self.sqrt_price_x96
        
        # 计算新的sqrtPrice
        numerator = liquidity * Q96
        denominator = liquidity * Q96 // sqrt_price + amount_in
        sqrt_price_next = numerator // denominator
        
        # 计算输出数量
        amount_out = liquidity * (sqrt_price - sqrt_price_next) // Q96
        
        # 更新池子状态
        self.sqrt_price_x96 = sqrt_price_next
        self.current_tick = self._sqrt_price_to_tick(sqrt_price_next)
        
        return amount_out
    
    def _swap_token1_for_token0_single_tick(self, amount_in: int, liquidity: int) -> int:
        """在单个区间内用token1购买token0"""
        sqrt_price = self.sqrt_price_x96
        
        # 计算新的sqrtPrice
        sqrt_price_next = sqrt_price + (amount_in * Q96) // liquidity
        
        # 计算输出数量
        amount_out = liquidity * (sqrt_price_next - sqrt_price) // sqrt_price_next
        
        # 更新池子状态
        self.sqrt_price_x96 = sqrt_price_next
        self.current_tick = self._sqrt_price_to_tick(sqrt_price_next)
        
        return amount_out
    
    def _get_current_liquidity(self) -> int:
        """获取当前区间的流动性"""
        current_tick_index = (self.current_tick // self.tick_spacing) * self.tick_spacing
        if current_tick_index in self.ticks:
            return self.ticks[current_tick_index]['liquidity_net']
        return 0
    
    def _get_next_initialized_tick(self, zero_for_one: bool) -> int:
        """获取下一个有流动性的tick"""
        current_tick_index = (self.current_tick // self.tick_spacing) * self.tick_spacing
        
        if zero_for_one:
            # 向下寻找
            next_tick = current_tick_index - self.tick_spacing
            while next_tick >= self.min_tick:
                if next_tick in self.ticks:
                    return next_tick
                next_tick -= self.tick_spacing
            return self.min_tick
        else:
            # 向上寻找
            next_tick = current_tick_index + self.tick_spacing
            while next_tick <= self.max_tick:
                if next_tick in self.ticks:
                    return next_tick
                next_tick += self.tick_spacing
            return self.max_tick
    
    def _compute_max_input_zero_for_one(self, sqrt_price: int, next_sqrt_price: int, liquidity: int) -> int:
        """计算在当前区间能消耗的最大token0数量"""
        return int((liquidity * Q96 * (sqrt_price - next_sqrt_price)) // (sqrt_price * next_sqrt_price))
    
    def _compute_max_input_one_for_zero(self, sqrt_price: int, next_sqrt_price: int, liquidity: int) -> int:
        """计算在当前区间能消耗的最大token1数量"""
        return int((liquidity * (next_sqrt_price - sqrt_price)) // Q96)
    
    def _cross_tick(self, tick: int, zero_for_one: bool):
        """跨区间操作"""
        if tick in self.ticks:
            # 更新当前tick
            self.current_tick = tick
            # 更新sqrtPrice
            self.sqrt_price_x96 = self._tick_to_sqrt_price(tick)
            
            # 更新流动性（简化处理）
            if zero_for_one:
                # 向下跨区间，减少流动性
                self.liquidity = max(0, self.liquidity - self.ticks[tick]['liquidity_net'])
            else:
                # 向上跨区间，增加流动性
                self.liquidity += self.ticks[tick]['liquidity_net']
    
    def get_current_price(self) -> Decimal:
        """获取当前价格（人类可读格式）"""
        return self.sqrtpx96_to_price(self.sqrt_price_x96)
    
    def get_pool_state(self) -> Dict:
        """获取池子当前状态"""
        return {
            'sqrt_price_x96': self.sqrt_price_x96,
            'liquidity': self.liquidity,
            'current_tick': self.current_tick,
            'current_price': float(self.get_current_price()),
            'fee_growth_global': self.fee_growth_global,
            'crossed_ticks': self.crossed_ticks.copy(),
            'active_ticks': list(self.ticks.keys())
        }


def create_pool_from_config(initial_price: float, initial_liquidity: int, fee_rate: float = 0.003,
                           tick_spacing: int = 60, min_tick: int = -887272, max_tick: int = 887272) -> V3Pool:
    """
    根据配置参数创建池子
    
    Args:
        initial_price: 初始价格 (USDC/ETH)
        initial_liquidity: 初始流动性
        fee_rate: 交易费率
        tick_spacing: tick间隔
        min_tick: 最小tick
        max_tick: 最大tick
        
    Returns:
        V3Pool实例
    """
    sqrt_price_x96 = V3Pool.price_to_sqrtpx96(initial_price)
    return V3Pool(sqrt_price_x96, initial_liquidity, fee_rate, tick_spacing, min_tick, max_tick)