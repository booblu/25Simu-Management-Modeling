# 🧠 Project 2 战术心法包 (Active LP Design Patterns)

> 本文档专为解决 P2 中最硬核的“调仓损耗（Impermanent Loss & Gas Friction）”与“Agent 主循环架构”而准备。

---

## 🏎️ 秘籍 1：如何在你的 Python 脚本中喂入真实世界？

在 P2 中，你将从 `00_Starter_Template` 里拿到一个真实历史 CSV (`experiments/data/weth_usdc_flash_crash.csv`)。
你要做的是写一个主循环函数，像时间机器一样播发这些订单。

```python
import pandas as pd
from src.simulator import V3Engine # 这是你在 P1 写的机器

def milestone_1_validation(csv_path: str):
    # 你的 P1 V3 引擎
    engine = V3Engine(initial_priceX96=...)  # 根据 CSV 第一行初始化
    df = pd.read_csv(csv_path)
    
    for index, row in df.iterrows():
        # 执行每一笔从真实世界扒下来的 Swap
        # row['amount0In'], row['amount1In']
        # row['zeroForOne'] 决定方向
        engine.execute_swap(
            zeroForOne=row['zeroForOne'],
            amountSpecified=row['amountSpecified']
        )
        
    print(f"你的终态价格: {engine.get_sqrtPriceX96()}")
    print(f"链上真实价格: {df.iloc[-1]['end_sqrtPriceX96']}")
    # assert 你的价格 == 链上价格
```

**⚠️ 防错警告 (Gotcha)：在真实世界，哪怕相差 $1 wei$ 的四舍五入，跑一万笔订单后价格都会走偏。你必须保证你的 P1 引擎绝对严苛吻合了白皮书的截断物理法则。**

---

## 💸 秘籍 2：无常损失与摩擦成本计算 (Impermanent Loss & Friction)

你的 Agent 有两个死敌：
1. **Gas Fee 摩擦 (Friction Cost):** 每次你做 `remove_liquidity` 和重新 `add_liquidity`，在以太坊主网上大概需要消耗 200,000 到 400,000 的 Gas 额度。
2. **无常损失 (Impermanent Loss/Divergence Loss):** 因为你在调仓时，价格已经变了。你总是以劣势的价格把剩下的劣势单边资产抽出来，然后被迫用更高的价格去买入另一种资产来配对进入新池子。

### 调仓结算通用核算公式
当你试图在 `Time(T)` 结清老池子，在 `Time(T+1)` 开启新池子时，你账户的美元本位 (USDC Base) 会经历这么一次折损：
```python
# 假设当前 Token0 = USDC, Token1 = ETH
def rebalance(agent_vault, current_price_Q96, target_tick_lower, target_tick_upper):
    # 1. 抽出旧资金 (Withdraw old liquidity)
    tokens_returned = engine.remove_liquidity(agent.position_id)
    agent_vault.balance0 += tokens_returned.amount0
    agent_vault.balance1 += tokens_returned.amount1
    
    # [利润点] 收取积累的 V3 交易费
    fees = engine.collect_fees(agent.position_id)
    agent_vault.balance0 += fees.amount0
    agent_vault.balance1 += fees.amount1
    
    # [流血点 1] 缴纳 Gas 打击 (模拟设定每操作一次直接扣减对应的 USDC 作为 Gas 折旧)
    GAS_FEE_IN_USDC = 50.00  # P2 我们把它当做一个恒定的外生参数，用来模拟高昂网络费
    agent_vault.balance0 -= GAS_FEE_IN_USDC
    
    # [流血点 2] 为了进入下一次极窄区间，资产需要强行配平
    # agent_vault 必须在当前的 current_price_Q96 市价下，抛售部分多余的 TokenX，买入 TokenY
    # 这必定产生无常与汇率滑点折扣！
    
    # 2. 注入新资金 (Add new liquidity)
    new_liquidity = calculate_liquidity_for_amounts(
        current_price_Q96, 
        target_tick_lower, target_tick_upper, 
        agent_vault.balance0, agent_vault.balance1
    )
    engine.add_liquidity(target_tick_lower, target_tick_upper, new_liquidity)
```

**你的首要任务是写一个 `Total_Wealth_Valuation(agent_vault, current_price)` 探针，随时在每个循环点计算你手里的 (USDC + ETH 现值 / 当前汇率)。**

---

## 🤖 秘籍 3：典型智能代理（Agent）策略阵型 (Tactical Patterns)

在撰写 `agent.py` 时，你可以采用以下设计模式（Design Patterns）：

### 1. 静态死守模式 (Static Dumb Baseline)
如同鸵鸟，任尔东南西北风。
设置极宽区间：`Tick[-887220]` 到 `Tick[887220]` (V3 全区间)。
- **优势：** 调仓 Gas 摩擦等于 0，绝不套现认输。
- **劣势：** 资金利用率等于 1/4000，别人赚 100 块息，你只能赚几毛钱。

### 2. 区间移动靶 (Trailing Range Rebalancer)
如果你预计大盘最近单边上涨，你可以设计一个条件触发机器：
```python
if current_price > (my_upper_tick_price * 0.95):  # 逼近上线抛售的死亡地带 5% 处
    # 紧急撤离并向上平移区间
    rebalance(...)
```
- **核心风险：** 如果这是个假动作（震荡市），你刚刚平移重整交了 50 刀 Gas 费，价格立马跌了回来。这就是“高频调仓被两头来回割肉（Whipsawed）”惨剧。

### 3. JIT 流动性狙击模式 (Just-In-Time MEV 进阶拓展)
- 能预测或扫描下一秒的巨大单（比如有个鲸鱼要抛售）。
- `step 1`: 你的 agent 在巨单到来前瞬移资金进池。
- `step 2`: 巨单成交，你的 Agent 虽然承受无常损失，但独吞了这笔巨单 100% 的高昂手续费。
- `step 3`: 你的 agent 立刻撤出资金跑路。
这是一场比拼延迟与算计的“核武器”，你将在 P2 的极压状态里证明这套打法的得失。

**记住，你是在跟物理法则做斗争。你的每次代码改动，都必须问自己：“我的 Agent 在交足 Gas 的前提下，到底赚不赚？”**
