"""
🔥 Project 2: 这个文件是你唯一允许写入 Agent "智商" 的地方。
"""

class AgentVault:
    def __init__(self, initial_usdc, initial_eth):
        self.balance_usdc = initial_usdc
        self.balance_weth = initial_eth
        self.position_id = None
        
    def get_total_wealth(self, current_price_usdc_per_eth):
        # ⚠️ 注意这里你可能要计算池子里的持仓价值加上你手头的现金
        pass

class BaselineAgent:
    """
    瞎子死守策略：上线第一天直接放置一个极其宽广的区间，然后永远不调仓，永远不交 Gas 费。
    """
    def __init__(self, vault: AgentVault):
        self.vault = vault

    def step(self, current_tick):
        # 永远返回不操作
        return {"action": "HOLD"}


class CandidateAgent:
    """
    智能调仓策略：你需要在这里写下何时触发调仓，何时认亏离场。
    """
    def __init__(self, vault: AgentVault):
        self.vault = vault

    def step(self, current_tick):
        # TODO: 编写你的策略逻辑
        # 例：if current_tick 逼近警戒线 -> 触发 remove_liquidity 和 add_liquidity
        return {"action": "HOLD"}
