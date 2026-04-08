# 🐺 Project 4 / Assignment 4: 黑暗森林的狩猎者 —— 多主体微观生态博弈 (Multi-Agent Micro-Market Game)

> **Sprint 4 交付倒计时：2 周**
> **能力象限：** 纳什均衡求解、Agent-Based Modeling (ABM)、机制逆向设计 (Mechanism Design)、帕累托最优帕累托分析。

---

## 🌍 这个世界，不是只有你一个人很聪明

在前三个 Project 中，无论是做市还是对冲，你的敌人都是“死物”——一长串历史订单 CSV。那叫做**单机游戏 (Man against Environment)**。

但在真实的去中心化世界里，**每个人都是像你一样的算法机器人**。
当你算出了一个极其完美的调仓 Tick 区间，准备赚取高额手续费时；一个**毒性套利者 (Toxic Arbitrageur/MEV)** 凭借比你快 1 毫秒的网速，抢先发现此时池子价格与币安交易所外部价格存在微小价差。他瞬间砸下天量大单，把你的本金套利抽干。
而在你亏本决定拔网线离开时，大量的**散户 (Noise Traders)** 又因为你的离开而面临高昂的滑点（由于池子变浅）。

**这叫公地悲剧 (Tragedy of the Commons)。**

这是本门课程的终局之战：你将跳脱出“逐利者”的身份，化身为这座黑暗森林的上帝——**协议缔造者 (Protocol Architect)**。
你要用工业界标准的 `Mesa` 框架搭建一个能容纳几百个机器人互砍的沙盒。先亲手验证他们是如何内卷致死并弄崩这个系统的，然后试图**修改底层参数**，拯救这个世界。

---

## 🗺️ 任务一览与里程碑 (Milestones)

### 🚩 Milestone 1: 创建物种档案 (The Agent Species)
在本次作业的 Starter Repo 中，必须拥抱正规军的 ABM 工业框架。你需要使用 Python 的 `Mesa` 库来定义三个物种。在 `src/agents/` 目录中：
- `noise_trader.py`：**噪音散户**。按照几何布朗运动或完全随机抛硬币，在引擎里发出买单或卖单，为系统无私地提供手续费。
- `arbitrageur.py`：**毒性套利者**。拥有透视外部真实价格 (Oracle Price) 的能力，当发现池子里价格偏离超过某阈值时，立刻做反向套利，抽取池子流动度。
- `smart_lp.py`：**内卷做市商**。基于你 P2/P3 写的组合，试图在最赚钱的地方扎堆。

### 🚩 Milestone 2: 点燃世界的火种 (The Environment Model)
- **任务目标：** 在 `master_model.py` 中，使用 `Mesa` 的调度器 (Scheduler，如 `RandomActivation`) 把所有机器人塞进你的 V3 模型里面。
- **让时钟走动：** 每运行一个 `step()`，所有特务都在这个大锅乱炖里发单。你要统计出每个周期的池子流动性深度 (L) 变化、系统总套利抽血量和 LP 的平均亏损额。

### 🚩 Milestone 3: 观测毁灭 (Observation of System Collapse)
- 运行 1,000 个时间步长（Tick）。
- 绘制图表证明一点：**当套利者资本变得无穷大，或者散户交易量枯竭时，所有 LP 即使搭载了完美的对冲算法，最后也会入不敷出宣告破产，纷纷下线。池子枯竭，系统死亡。**

### 🚩 Milestone 4: 上帝的救赎 —— 机制修改试验 (Mechanism Design Proposal)
这是全课的最重头戏！打开你从 P1 一路原封不动用到现在的 `simulator.py`。
作为协议创始人，赋予你修改“神圣物理法则”的权力！
请进行至少一项重大修改（例如）：
1. **动态费率防御：** 当池子在短时间内价格偏移剧烈时，把交易费从固定 0.3% 突然拉爆成 5.0%，防守 MEV 套利。
2. **非对称调仓费：** 或者对大资金 LP 的提款收税。

重新跑一遍所有的机器人。证明你的新机制让 LP 重新赚到了钱，生态恢复繁荣。

---

## 🎖️ 评分标准 (Rubric) - 满分 100 分

### 1. 多智能体架构规范化 (Mesa implementation) [30%]
- [x] 能否极其规范地继承了 `mesa.Agent` 和 `mesa.Model`？
- [x] 代码跑通了 `mesa` 独特的数据收集器 (DataCollector)，严密抓取了上帝视角的宏观经济指标。

### 2. 生态博弈演绎逻辑 (Emergence Demo) [20%]
- [x] 成功再现了“劣币驱逐良币”的死亡螺旋现象。

### 3. DAO 治理提案 - 黑皮书 (The God-Mode Policy Memo) [50%]
- **注意：决胜分 50% 全在这篇你写的万字级/千字级别 README 备忘录里。**
- [x] **缺陷定罪：** 向所有以太坊理事会成员（你的同学就是你的投资人）证明 V3 极度死板的费率存在的结构性剥削缺陷。
- [x] **机制主张：** 说清楚你修改了哪几条物理法则？这些改动在何种程度上逼近了**帕累托最优 (Pareto Optimality)**？（要用你的对比回测跑分图表作为唯一证据）。

---

## 📦 你的工具库 (Starter Kit)
1. 作业代码获取：*(等待教官下发 Github Classroom P4 邀请链接)*
2. 战术心法图册：[Project4_MultiAgent_Patterns.md](../04_Resources/Project4_MultiAgent_Patterns.md) (详细拆解了 Mesa 引擎的接入指南以及如何写出合格的提案备忘录)。
