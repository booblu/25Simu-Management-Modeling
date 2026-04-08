# 📢 课程作业与通知群发档案 (Broadcast Archive)

本文档专门用于存放历次向班级微信群、Canvas 或 Blackboard 发布的**群发公告模板**。
建立此档案库的目的：将“师生沟通”也视为一项工程，实现标准化的 SSSOT（Single Source Of Truth），确保明年的助教（TA）可以直接复用。

> **注意：** 当向学生群发链接时，请务必核对当年的 GitHub Classroom `invitation_link` 是否已更新。

---

## 🎯 Project 1：V3 状态机模拟 (发布通知)
*发送时机：Week 1 (Kickoff 结束后)*
*渠道：微信班级大群 / 课程公告栏*

### 【V2 - 朴实无华版】(建议使用)
*(清晰、克制、聚焦于学生交付的 4 个核心动作)*

**各位同学好，Project 1（Uniswap V3 底层状态机模拟）作业已正式发布。**

这是本课程的第一个核心项目，请大家按照以下步骤开展工作：

**1. 领取你的专属代码仓库**
请点击下方的 GitHub Classroom 邀请链接，系统会自动为你创建一个私有的作业仓库：
👉 `https://classroom.github.com/a/suEX8PmT`
*(点击后请耐心等待几秒种，系统会自动帮你克隆好基础的代码脚手架。这个你的私人仓库，只有你和助教能看到。)*

**2. 去哪里看作业要求？**
在你自己的沙盒仓库里**没有**作业要求文件。本课程所有的作业要求和考核标准（Rubric），统一在我们的“课程主页面”进行更新和维护。
请务必仔细阅读：[Project1_V3_State_Machine.md](https://github.com/booblu/26Simu-Management-Modeling/blob/main/03_Assignments/Project1_V3_State_Machine.md) ，里面明确写了我们要实现的最低功能（MVP）是什么，以及千万不要去写哪些超纲代码。

**3. ⚠️ 老师的两条防坑死命令（非常重要）：**
大家在具体写 Python 代码和询问大语言模型（AI）时，必须要避开以下两个致命坑：
- **关于计算精度**：智能合约的底层是没有小数点的。严禁在这份作业里使用 Python 的 `float` 或者 `decimal` 进行底层状态换算（会产生极大的幻觉误差）。必须使用 Python 的自带大整数（BigInt）进行向右 96 位（$Q64.96$）的位运算。**不知道怎么写的，先去看 [这本 Math Cheat Sheet 作弊手册](https://github.com/booblu/26Simu-Management-Modeling/blob/main/04_Resources/Project1_V3_Math_CheatSheet.md)。**
- **关于如何正确使用 AI**：请不要泛泛地去问 AI“帮我写个 Uniswap 交易公式”，它大概率会给你写错。你必须要去看 [**项目期阅读清单**](https://github.com/booblu/26Simu-Management-Modeling/blob/main/04_Resources/Project1_V3_ReadingList.md) 里老师给你们列出来的**真正的 Solidity 官方源码库 (UniswapV3Pool.sol)**。正确的做法是：**把 Solidity 源码复制给 AI，让它帮你 1:1 翻译成没有误差的 Python 代码！**

**4. 应该怎么交作业？**
不需要发邮件交压缩包。只需要完善好你们仓库里的 `simulator.py`、写好断言测试 `test_invariants.py`，最后推送到云端 (`git push`)。GitHub 会自动运行里面的 `ci.yml` 帮你判分。看到绿色的对勾就代表物理断言通过了！

有遇到不懂的报错环境，随时在群里发截图讨论。祝大家顺利！

---

### 【V1 - 硬核战役版】(备用)
*(带有强烈的 CTO 视角代入感，适合营造紧张和严肃的工程氛围)*

**【Mission Alert】Project 1：V3 底层状态机极限沙盘 已正式上线！**

各位 CTO 们，你们的第一个硬核战役打响！
未来的 8 周，你不需要写任何 Word 废话报告，所有的考核都在绝对客观的代码生死线之上，机器就是裁判。

🔥 **点击下方唯一行动指令，领取你的专属私有量化车间：**
👉 `https://classroom.github.com/a/suEX8PmT`
*(点击后，GitHub 会为你直接克隆出一个极其纯净的防弹沙盒仓库。)*

**在你的沙盒里敲下第一行代码前，必须完成以下这 4 步“战前检阅”，否则必死无疑**：
1. **宏观目标**：去这门课唯一的主权级文档库 [26Simu-Management-Modeling](https://github.com/booblu/26Simu-Management-Modeling) 
2. **生死边界**：仔细研读 `03_Assignments/Project1_V3_State_Machine.md`。看看本周你要交付哪几个红线功能（MVP），以及不准碰哪些“毒药区”。
3. **破除幻觉**：V3 底层完全没有小数概念！在你对它的算账逻辑感到绝望时，请绝对服从 `04_Resources/Project1_V3_Math_CheatSheet.md`。这套作弊心法里藏着你们保命的 $Q64.96$ 位运算军规。凡是被 CI 扫出使用 `float` 做核心倒数运算的，直接 Fail。
4. **硬核原著**：推导跨区间交易逻辑时，遇到问题不要去搜百度的博客。请直接打开 `04_Resources/Project1_V3_ReadingList.md`，那里置顶了全网唯一的真相——**UniswapV3Pool.sol (源码)**，把你读不懂的源码发给 AI 让他帮你翻译成 Python。

把你们的逻辑抽屉造好，把物理断言（Invariants）写满 `tests/`。只要 `git push` 后云端的 CI 亮起绿色的对勾，你们就可以安稳入睡，等待 Demo Day 的路演大审判。

祝极压测试武运昌隆！

---

## 🎯 Project 2 (发布通知)
*发送时机：Project 1 截止，Project 2 沙盘正式下发时*
*渠道：微信班级大群 / 课程公告栏*

各位同学，大家好：

Project 2（Active LP 策略仿真）的作业代码环境现已发布。

在接下来的两周时间里，我们将基于大家在 Project 1 中搭建完成的底层算账引擎，进一步引入真实的链上数据和调仓摩擦成本，开发你们的第一套自动做市策略（Agent）。

🔗 **Project 2 代码仓库领取链接：**
👉 `https://classroom.github.com/a/_0XKL2cK`

### 📋 本次作业的核心要点与规范：

1. **环境迁移规则（必须遵守）：**
   本次作业会为大家生成一个全新的沙盒分支，但其中**不包含**核心算账引擎。
   请大家在克隆新仓库后，**手动将你在 Project 1 中写好的 `simulator.py` 文件复制并粘贴到新仓库的 `src/` 目录下**。你的新策略将完全依赖你的旧引擎运行。如果之前的引擎还存在未修复的 Bug，你的策略回测将会报错。这要求大家持续为自己的底层系统负责。
2. **数据处理要求：**
   本次作业不提供打包好的现成历史数据集。大家需要前往 Dune Analytics 或使用 The Graph 等工具自行提取真实数据。
   - **指定数据切片：** 2021 年 5 月 19 日 00:00 至 23:59（UTC）。
   - **指定目标对象：** 以太坊主网 USDC/WETH 0.3% 池。
   你们需要把这 24 小时内的真实 Swap 交易单导出为 CSV。具体如何根据原始日志的正负号来推算交易方向（zeroForOne），请参阅下发的 `Project2_Active_LP_Patterns.md` 指南。
3. **摩擦成本的计算：**
   本次作业要求实现两套测试策略（静态基准策略 vs 动态调仓策略）。请特别注意：程序中每次执行移除和添加流动性的重平衡动作时，你们的账户虚拟资金必须扣除相应的 Gas 手续费，并准确结算无常损失。不考量摩擦成本的乌托邦系统不予及格。
4. **作业最终交付：**
   除了代码必须跑通 Milestone 1 的数据回测断言外，你们还需要在沙盒的 `README.md` 中提交一份不超过一页纸的《高管决策备忘录》（Decision Memo）。请结合你们程序生成的收益曲线图表，客观分析你的智能 Agent 在剧烈单边波动行情下失败（产生巨亏）的边界条件是什么。

有任何获取数据或代码调试上的共性问题，随时在群内发截图讨论。祝大家顺利！

---

## 🎯 Project 3 & Project 4 (课程后半程群发通知板)

### 📌 Project 3: 跨越深渊的桥梁 (Delta Neutrality) 发布通知
*发送时机：Project 2 截止后*

各位 CTO，Project 2 的血火考验结束了。
无论你的调仓 Agent 写得多聪明，当面临 5.19 的系统性暴跌时，纯粹的多头敞口（Long Bias）依然会让净资产惨遭腰斩。为了在这个死亡森林里寻找圣杯，本周我们进入 Project 3：**多协议跨链对冲组合（Cross-Protocol Delta Neutrality）**。

🔗 **Project 3 代码仓库领取链接：**
👉 `[教官在此粘贴 GitHub Classroom 生成的邀请链接]`

**⚠️ 这次你们要手撕两台印钞机：**
1. **自己造一家去中心化银行 (Aave Mock)：** 请在 `src/aave_mock.py` 里自己写一套带抵押率计算、生息、借钱和连环清算大审判的借贷机器。
2. **上帝视角的组装：** 通过抵押 USDC 借出 ETH 开空单（Short Delta），并把它和你们的 P1 V3 机器（Long Delta）打包缝合在一起。
你们的终极目标，是在大盘再次暴跌时，画出一条令华尔街侧目的**绝对水平净值曲线**（赚取手续费，但抹平暴跌无常损失）。

祝你们的资产负债表金枪不倒！

---

### 🐺 Project 4: 黑暗森林的狩猎者 (Multi-Agent Game) 发布通知
*发送时机：Project 3 截止后，课程期末阶段*

各位协议架构师，这是本课程最后，也是见证最高级“涌现（Emergence）”时刻的毕业战役。
把你们之前的单机游戏全部推倒！现在，你的池子将被扔进一个无主之地，并注入上百只机器狗（噪音散户 vs 有毒套利者 MEV vs 极致内卷同行）。

🔗 **Project 4 取筹链接：**
👉 `[教官在此粘贴 GitHub Classroom 生成的邀请链接]`

**📋 最终极的考验：**
这不仅仅是教你用 `Mesa` 框架来搭沙盒。这是这门课的管理学灵魂大考：用代码撰写基于 ABM（Agent-Based Modeling）的**机制逆向设计报告（DAO Proposal）**。
你们要证明池子里的利润是如何被 MEV 抽干的（公地悲剧）。然后，通过修改你们自己的 V3_Engine 底层代码（比如添加动态费率、加税），挽救这个原本会死掉的池子生态。

**期待你们万字千金的上帝视角备忘录。武运昌隆！**
