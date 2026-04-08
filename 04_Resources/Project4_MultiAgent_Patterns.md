# 🧠 Project 4 战术心法包 (Mesa ABM & Mechanism Design)

> “你不再是一个玩家，你就是这场游戏的缔造者。”
> 本文档专门为了帮助你打通工业级标准 Agent-Based Modeling 框架 **`Mesa`** 的任督二脉，并教会你如在模型里抽取极宏观的经济学参数来撰写机制辩护（DAO Proposal）。

---

## 🏗️ 秘籍 1：Mesa 引擎接线指南 (The ABM Architecture)

在 P1 到 P3，因为只有我们自己的一个单体 Agent 在活动，我们可以随便用一个 `for t in time_series:` 把它打发了。
但在 P4，池子里有 100 个互不相让的智能体，而且他们发单的先后顺序极其重要（先发单的可能拿到好价格，后方直接被滑点收割）。这就必须启用**学术正规军 `Mesa`** 里的**调度器 (Scheduler)**。

你需要写一个主神类 `V3MasterModel`，继承自 `mesa.Model`。

```python
import mesa
from src.simulator import V3Engine # 你的老朋友

class V3MasterModel(mesa.Model):
    def __init__(self, N_noise_traders, N_arbitrageurs, N_smart_lps):
        super().__init__()
        # 把 V3 这台机器当作公共的上帝全知资产，放在 Model 最顶端
        self.v3_engine = V3Engine(initial_sqrtPriceX96=...)
        
        # 定义时钟引擎器。RandomActivation 意味着每一回合，系统会打烂所有Agent的顺序，随机点名发单。
        self.schedule = mesa.time.RandomActivation(self)
        
        # 批量造人运动
        for i in range(N_noise_traders):
            # 伪代码：注入噪音散户
            a = NoiseTrader(unique_id=i, model=self)
            self.schedule.add(a)

        # 重点指标记录针：这是你能否用数据证明机制优劣的关键！
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Total_Liquidity": lambda m: m.v3_engine.get_total_liquidity(),
                "Oracle_Divergence": lambda m: abs(m.v3_engine.get_price() - external_oracle_price)
            },
            agent_reporters={
                "Agent_Wealth": "wealth"
            }
        )

    def step(self):
        """主神按下了前进 1 分钟的按钮"""
        # 第一步：必须要收集此时的各类宏观和微观体征数据
        self.datacollector.collect(self)
        # 第二步：让下面所有的 100 个 Agent 开始这回合的厮杀和发单
        self.schedule.step()
```

---

## 🤖 秘籍 2：物种原型的定义格式

每一个在这里谋生的交易员或者机器人，都必须继承自 `mesa.Agent`。

```python
class NoiseTrader(mesa.Agent):
    def __init__(self, unique_id, model):
        # 这里的 model 就是指上面的 V3MasterModel，让探员随时能访问公共环境
        super().__init__(unique_id, model)
        self.wealth = 10000 
        
    def step(self):
        # 【你的核心战役】：根据概率丢硬币。
        # 如果是抛字面，就从自己兜里拿钱，向 self.model.v3_engine 提交一笔 Swap 卖单
        pass
```
**挑战：** 这个沙盒里的套利者(`Toxic Arbitrageur`) 并不是抛硬币，而是具备预言家能力的收割机。他在自己的 `step()` 里需要窥探外部预言机（你可以生成一个随时间游走的随机游走序列当黑天鹅走势），然后用最狠的买/卖量抹平跟 V3Engine 里的差价。如何写出最狡猾的套利逻辑？看你的了。

---

## 📜 秘籍 3：机制黑皮书的标准范式 (The Pareto Optimal Memo)

我们要求你在完成代码后，像真正的顶级 DAO （去中心化治理）研究员撰写一份 **Mechanism Implementation Proposal**。不要写流水账，请严格包括以下三个板块：

### 1. The Broken System (系统脆弱性证实)
- 先运行包含固定手续费的原版 `simulator.py`。
- 展示你生成的表格和截图（例如，散户不断交易，但利润全部被套利者赚走，LP一直在亏损，最后导致 `Total_Liquidity` 这个你在 `DataCollector` 里抓取的值趋近于0）。
- 定罪：**当前的 V3 是结构性脆弱的。**

### 2. The God's Intervention (机制魔改主张)
- 讲解你修改了什么样的源代码。
- **高阶灵感：你可以引入挂单时间锁定延时器，或者对超过 5% 的滑点单课征一笔“巨鲸滑点惩罚费”，再由这笔额外的罚红反哺给辛苦的 LP。**

### 3. Pareto Analysis (帕累托验证)
- 重新跑相同的 100 个 Agent 十万次 `step()`。
- 放出新的数据走势曲线证明：这套改版机制虽然稍微提高了对散户或 MEV 的惩罚门槛（损害了一方利益），但是让 LP 避免了灭绝式的撤资。这在经济学上促成了生态的正向循环涌现。
