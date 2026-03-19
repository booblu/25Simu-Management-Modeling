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
