# 📚 项目 1 (第 1–2 周) 阅读资料清单 (V3 架构版)

**主题：Uniswap V3 协议机制建模与离线仿真 (Protocol as State Machine)**  
*(本清单专供 Project 1 使用。请按“必读 → 必读 → 必读”的扫雷顺序完成，切勿一开始就陷入无边无际的网络文章中。)*

---

## 🎯 这两周你要完成什么（读资料前先看）
你要做的不是“写一份关于 DeFi 的研报”，也不是“学习 Solidity 写智能合约”。你要完成的是工程挑战：

- 把真实的 **Uniswap V3（集中流动性）智能合约** 抽象成一个**离散数字刻度下的可计算系统**：状态（Ticks/当前价格/全局手续费） + 事件（Swap跨区间） + 约束（不变量）。
- 写出极具摧毁性的**不变量/边界测试 (Invariants Tests)**，并让它们在 GitHub CI 中自动运行。
- 用代码证明：在经历单边暴跌连续击穿 10 个 Tick 后，你算出来的资金池余额和扣留的手续费，在 `1e-12` 精度下丝毫不差。

---

## 🅰️ 协议物理法则必读（保证“机制正确”）

> **目标**：看完能把 Uniswap V3 的“集中流动性”规则，降维成代码里的 `Current_Tick` 与数组变化。

1) **Uniswap V3 Core Whitepaper (硬核官方白皮书 - 必须看原著)**  
- **看什么**：全网唯一讲透为什么不用小数的圣经。直接翻到公式 6.13 到 6.15，这就是你要写进代码的物理方程。
- **参考**：[Uniswap v3 Core Whitepaper (PDF)](https://uniswap.org/whitepaper-v3.pdf)

2) **Uniswap V3: Concentrated Liquidity (集中流动性核心概念)**  
- **看什么**：理解为什么资金不再是均匀平铺，而是被锁定在特定的价格抽屉（Tick）里。
- **看完能回答**：当价格不在某个 Tick 区间时，那个区间里的资金在干什么？
- **参考**：[官方概念指南 - Concentrated Liquidity](https://docs.uniswap.org/contracts/v3/concepts/core-concepts/concentrated-liquidity)

2) **Uniswap V3: Architecture & Ticks (系统架构与刻度)**  
- **看什么**：理解价格是如何被切分成一个个离散的 Tick 的，跨越 Tick 时发生了什么。
- **看完能回答**：为什么你的模拟器在处理 Swap 时，如果一笔大单耗尽了当前 Tick 的流动性，必须分步骤进入下一个 Tick？
- **参考**：[官方架构解析 - Architecture](https://docs.uniswap.org/contracts/v3/concepts/core-concepts/architecture)

3) **Uniswap V3: Fees (手续费的微积分)**  
- **看什么**：V3 的手续费不再像 V2 那样简单放入大池子，它是如何精准分配给当时“正在服役”的流动性的？
- **看完能回答**：如何用代码测试证实手续费一点没被贪污，且完全分配给了处于激活区间（In-Range）的 LP？
- **参考**：[官方费用详解](https://docs.uniswap.org/contracts/v3/concepts/advanced-topics/fees)

---

## 🅱️ 验证与可复现必读（把“不变量”变成机器法官）

> **目标**：能写出自洽的《建模规格书（Model Spec）》以及对应的 `tests/test_invariants.py`，让云端 CI 机器人自动验收你的个人产品引擎。

4) **pytest: Get Started (自动化测试入门)**  
- **看什么**：如何创建测试、运行测试、读懂满屏的红字报错。
- **看完能做到**：敲下 `pytest` 命令，看着你的 V3 数学引擎全部亮起绿灯。
- **参考**：[pytest official](https://docs.pytest.org/en/stable/getting-started.html)

5) **pytest: Assertions (断言与生死线)**  
- **看什么**：如何在 Python 中写下不可逾越的红线（如 `assert pool_balance >= 0`）。
- **参考**：[pytest asserts](https://docs.pytest.org/en/stable/how-to/assert.html)

6) **GitHub Actions: Building and testing Python (云端结界 CI)**  
- **看什么**：如何让每一次 Push 都在云端自动触发你的测试脚本。
- **看完能回答**：为什么课程强调 CI 门禁？（答：消除“在我的电脑上明明能跑”的工程借口）。
- **参考**：[GitHub Actions Docs](https://docs.github.com/actions/guides/building-and-testing-python)

---

## 🅲 实验输出与数据作图（产出你的弹道报告）

> **目标**：能把千万次循环交易后的数据抽离出来，画成《资金利用率曲线图》。

7) **pandas: 读写 CSV (构建 metrics.csv)**  
- **看什么**：`to_csv` 基础用法，将仿真的日志固化。
- **参考**：[Pandas Read/Write](https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html)

8) **matplotlib: 基础图表绘制**  
- **看什么**：如何把 pandas 里的价格变动与无常损失画成折线图。
- **参考**：[Matplotlib Simple Plot](https://matplotlib.org/stable/gallery/lines_bars_and_markers/simple_plot.html)

---

## 🅳 极客选读 (高阶开荒者专区)

9) **Uniswap V3 Math (硬核数学原理)**  
- **适合人群**：你想完全搞懂 V3 背后 `sqrtPriceX96` 那些变态的位运算和精度控制原理。
- **参考**：[Uniswap V3 Math Primer](https://plutus.art/understanding-uniswap-v3-math/)

10) **Hypothesis (Property-based Testing 模糊测试)**  
- **适合人群**：你想让机器像疯子一样自动生成几万个随机奇葩订单，来摧毁你的仿真系统，以证明你的系统无懈可击。
- **参考**：[Hypothesis Documentation](https://hypothesis.readthedocs.io/)
