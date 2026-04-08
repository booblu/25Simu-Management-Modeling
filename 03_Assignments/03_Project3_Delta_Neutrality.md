# ⚖️ Project 3 / Assignment 3: 跨越深渊的桥梁 —— 多协议 Delta 中性对冲仿真 (Cross-Protocol Hedge)

> **Sprint 3 交付倒计时：2 周**
> **能力象限：** 资产负债表拆解、Delta 敞口计算、超额抵押与清算断言、跨系统降维抽象。

---

## 🌪️ 深渊的凝视：如何打破不可战胜的系统性风险？

在 Project 2 中，你们已经尽最大努力写出了高频智能调仓代理（Active LP Agent），试图在剧烈的市场中寻找微弱的 Alpha。
但是，如果你回顾 P2 的最终净值图（Total Wealth Trajectory），你会发现一个绝望的物理定律：**不管你的调仓算法有多智能，只要以太坊大盘遭遇深 V 断崖式下杀，你的总净值依然会跟着市场一起跌落。** 因为你是天然的“多头（Long Bias）”。

为了解决这个根本性的灾难，金融工程师们发明了**“Delta 中性（Delta Neutrality）”**。
只要你的总敞口 (Delta) 为 0，大盘怎么暴跌都不关你的事，你依然能闭着眼睛稳赚 V3 的高额手续费。
但为了做到这点，你在把美元和 ETH 存入 Uniswap 之前，你的 ETH **不能是自己花钱买的，而必须是借来的**。因为借来的资产在暴跌时，你还款的法币成本也同步暴降，这就形成了完美的做空对冲（Hedge）。

所以，本期 Project 的终极决战：你不仅仅要跟 Uniswap 打交道，还要像“缝合怪”一样，同时调用另外一个去中心化借贷系统的引擎（如 Aave）。你的 Agent 必须升级为统揽全局的**跨协议投资组合管理人 (Portfolio Manager)**。

---

## 🗺️ 任务一览与里程碑 (Milestones)

### 🚩 Milestone 1: 徒手造轮子 —— 手搓 Aave 结算引擎 (The Lending Machine)
在本课，我们绝不依赖黑盒。要真正理解“为什么对冲会翻车”，你必须亲手制造一个印借条的引擎。
- **任务目标：** 在 `starter/src/aave_mock.py` 中编写一个微型的超额抵押借贷系统。
- **必须实现的接口与状态物理量：**
  - 【状态】记录用户的 `collateral_balance` (美元抵押物) 和 `debt_balance` (借出的 ETH 数量)。
  - 【动作】`deposit()`（存入抵押）、`borrow()`（生成债务）、`repay()`（偿还债务）。
  - 【断言 1】**健康因子护城河 (Health Factor):** 借钱时必须计算 `(抵押物总价值 * 抵押系数) / 总负债价值`。如果算出来 `< 1.0`，系统必须 `Raise Exception` 拒绝放款。
  - 【断言 2】**死神降临 (Liquidation):** 提供一个定时扫描函数，如果有人的健康因子在跌市中跌破了 `1.0`，他的抵押物将被强制清零，这叫连环爆仓。

### 🚩 Milestone 2: 资产负债表的拼图 (Portfolio Manager Agent)
既然你已经有了两台引擎（你在 P1 写的 `V3Engine` + 你在 P3M1 写的 `AaveMock`），现在你要写一个能同时操纵两台机器的高级总管。
- 当你的模型决定在 V3 开一个 LP 仓位，且需要投入 `N` 个 ETH 时。
- 你的 `PortfolioAgent` 会自动拿着你兜里的原始 USDC 去 `AaveMock` 抵押，借出正好等于 `N` 的 ETH。
- 然后把借来的 ETH 与剩下的 USDC 统统打进 `V3Engine`。
- **目标：系统整体持平（Delta ≈ 0）**。

### 🚩 Milestone 3: 穿越黑天鹅 (Surviving the Black Swan)
- 提取你 P2 中跑崩的“5.19 暴跌”数据，或者找一段更暴烈的下杀横盘组合。
- 同时开启无对冲的 P2 模型 和 加入了借贷对冲的 P3 模型。
- 提供回测证明：在支付了高昂的 Aave 借款利息（APY）且大盘暴跌时，P3 模型保住了本金。

---

## 🎖️ 评分标准 (Rubric) - 满分 100 分

### 1. 跨异构系统的连环性测试 (Cross-Engine V&V) [30%]
- [x] `test_milestone_1.py` 全绿。断言系统能完美执行“抵押、安全借贷、价格暴跌、触发强制清算边界”这一完整闭环。如果你的引擎连清算边界都算错，整个系统就是废纸。

### 2. 对冲逻辑与计算精度 (Hedging precision) [30%]
- [x] 能不能在 `PortfolioAgent` 里精准算出每一刻你在 Aave 的利息欠款？
- [x] 能不能精准展示你同时在这两台机器里（Aave抵押品 - Aave债务 + V3头寸总计 + V3已收利息）加总出来的唯一的系统总净值？

### 3. 可视化图表反转 (The Delta-Neutral Visualization) [20%]
- [x] 你的回测脚本要画出一张能一目了然看懂的图表，必须包含：大盘价格折线图（瀑布级暴降），P2 无对冲组合的净值（暴降），P3 对冲组合的净值（横向平稳，甚至略微上翘赚钱）。

### 4. 高管“一页纸”重症风控备忘录 (Risk Management Memo) [20%]
- 在 `README.md` 里撰写。
- [x] 作为风险控制总监，向 CEO 说明：虽然我们的系统已经是神奇的“Delta中性”绝不赔本了，但在今天这个 P3 架构下，**还有哪三种极端的连环崩盘场景**，会导致公司破产？
- **线索剧透 (Spoilers):** 去算一算你的抵押资产健康因子（Health Factor）的“缓冲区红线”设在哪里？如果插针行情导致来不及补保证金呢？

---

## 📦 你的工具库 (Starter Kit)
1. 作业代码获取：*(等待教官下发 Github Classroom P3 邀请链接)*
2. 战术心法图册：[Project3_Delta_Neutrality_Patterns.md](../04_Resources/Project3_Delta_Neutrality_Patterns.md) (详细阐述了 LTV 参数折算体系与 Delta 对冲的具体数学模型)。
