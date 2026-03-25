# 🎯 Project 2 / Assignment 2: 第一代拓荒者 —— 基于 V3 的主动做市 LP 策略仿真 (Policy on Protocol)

> **Sprint 2 交付倒计时：2 周**
> **能力象限：** 策略抽象、时间序列模拟、摩擦成本计算、风险边界 (ECR) 绘制。

---

## 💣 真实世界的毒打：你在对抗什么？

在 Project 1 中，你已经成功用 Python 复现了 Uniswap V3 的物理法则（底层状态机）。那是一台静态的机器。但在真实的黑暗森林中，价格每秒钟都在剧烈波动。
如果你像 V2 时代一样，把资金铺满整个价格区间（0 到 $\infty$）：你几乎赚不到什么手续费，资金利用率极低。
如果你把资金极其精明地锁定在当前价格附近的极窄区间（Concentrated Liquidity）：**只要价格稍微波动跌出你的区间，你将停止赚取任何手续费，并且会以最差的价格被迫清仓单边资产（遭遇极大的无常损失 Impermanent Loss）。**

为了解决这个窘境，你需要开发一个**主动做市代理（Active LP Agent）**：当系统价格快要跌出你的赚钱区间时，Agent 会自动抽出资金，在新的价格附近重新建立区间（Rebalance）。
但是，**每次调仓都需要向以太坊矿工支付极其高昂的 Gas 费！**

本期作业的核心冲突：**如何在“最大化赚取手续费”与“最小化调仓 Gas 摩擦成本 + 无常损失”之间，找到那套数学意义上的最佳调仓策略？**

---

## 🗺️ 任务一览与里程碑 (Milestones)

### 🚩 Milestone 1: 真实世界的 V&V (Verification & Validation)
在你运行任何聪明策略之前，你必须证明你的 P1 引擎能在真实数据下存活。
去你自己的沙盘（Starter Repo）的 `experiments/data/` 目录下，找到老师为你准备的一份真实的链上交易流 CSV。
- **任务目标：** 编写一个循环脚本，逐条读取这段长达几百行的 Swap 历史数据，并原封不动地 `execute_swap()` 打进你拷过来的 P1 `simulator.py` 中。
- **存活断言：** 循环结束后，对比你的引擎计算出的最终 `sqrtPriceX96`，是否与 CSV 库中记录的真实以太坊区块里的最终价格**完全一致（包含精度截断）**？
- *通关奖励：你的 P1 引擎正式被确认为“军工级”，可以承载巨量资金策略了。*

### 🚩 Milestone 2: 构筑两套对立的智能代理 (Agents)
利用验证完毕的循环结构，在 `agent.py` 中创建你的策略：
- **Baseline Agent (宽幅死守者):** 一个绝对懒惰的 Agent。在 Day 1 把流动性设置在当前价格的 ±30% 范围，然后去海滩度假，期间永远不调仓，任由本金被无常损失吞噬或停止赚息。
- **Candidate Agent (高管设计的智能猎手):** 由你自己设计的触发式 Agent。例如设计双布林带（Bollinger Bands），当价格触及特定阈值时，触发 `remove_liquidity()` 然后在最新价格附近立刻 `add_liquidity()` 追踪吃息。

### 🚩 Milestone 3: 摩擦成本与资金曲线绘制
为你的每次 `remove` 和 `add` 动作挂载一笔固定的 Gas 罚金（具体数值查阅 `Math_CheatSheet`）。
通过运行两种 Agent，使用 `matplotlib` 或 `seaborn` 绘制出两类 Agent 在给定时间序列内的**资金总价值曲线（Total Wealth Trajectory = TokenX Value + TokenY Value + Collected Fees - Gas Paid）**。

---

## 🎖️ 评分标准 (Rubric) - 满分 100 分

### 1. 引擎与数据重塑 (Foundation) [20%]
- [x] 能将 P1 的代码无缝拷入 P2。
- [x] `test_milestone_1.py` 必须跑通，证明你的引擎能完美消费真实的 On-Chain CSV 大数据流并精准抵达最终价格，没有浮点数幻觉爆仓错乱。

### 2. 策略代理实现 (Policy Implementation) [30%]
- [x] `Baseline Agent` 的逻辑构建（设置区间、计算收益）。
- [x] `Candidate Agent` 包含清晰的调仓触发逻辑（Trigger Logic）。
- [x] 你的代码能正确处理跨 Tick 的重平衡，并在代码里完美减损了**调仓摩擦（Gas 费）**。

### 3. 可视化与极压验证 (ECR Frontier) [20%]
- [x] 代码生成一套至少包含以下三条线的时间序列图表：
  1. 标的资产本身的市场价格走势（大盘图）。
  2. Baseline Agent 的净资产走势。
  3. Candidate Agent 的净资产走势。
- [x] 你是否证明了：在震荡市，高频短距调仓最赚钱；但在单边黑天鹅市，高频调仓会被 Gas 和无常损失反复割肉，死得最快？

### 4. 高管“一页纸”决策备忘录 (Decision Memo) [30%]
- **在你的 GitHub 面板的 `README.md` 中作答。字数极大限缩，不准写八股文。**
- [x] 解释你的 Candidate Agent 的核心假设边界是什么？
- [x] 根据你的图表数据，作为 CTO，请向董事会证明：在什么特定的市场波动率下，你设计的调仓机器人会导致致命的亏损（所谓“倒大霉”的极端条件）？

---

## 📦 你的工具库 (Starter Kit)
1. 作业代码获取：*(群内等待教官下发 Github Classroom 邀请链接)*
2. 战术心法图册：[Project2_Active_LP_Patterns.md](../04_Resources/Project2_Active_LP_Patterns.md) (详细拆解了如何用 Python 计算无常损失以及如何写标准的 Agent Loop)。
