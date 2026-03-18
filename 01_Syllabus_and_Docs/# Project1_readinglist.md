# 项目 1(第 1–2 周)阅读资料清单  
**主题:Uniswap v2 协议建模与离线仿真(Protocol as System)**  
(本清单用于项目 1。请按“必读 → 必读 → 必读”的顺序完成,不需要在网络资料里扩展阅读。)

---

## 这两周你要完成什么(读资料前先看)
你要做的不是“链上开发”,也不是“交易/投资分析”。你要完成的是:

- 把 Uniswap v2 抽象成一个**可计算系统**:状态(储备/价格/手续费/LP份额) + 事件(swap 等) + 约束(不变量)
- 写出**不变量/边界/可复现**的测试(tests),并让它们在 CI 中自动运行
- 设计至少 6 个情景(scenarios),一键运行后输出 `metrics.csv` 和图表
- 用证据回答:**协议在什么情景下最脆弱?什么情景下最稳?**

---

# A. 协议必读(必须看:保证“机制正确”)

> 目标:看完能把 Uniswap v2 的关键规则翻译成“状态变量 + 状态更新 + 约束检查”。

1) **Uniswap v2:How Uniswap works(协议如何工作)**  
- 看什么:恒定乘积 `x*y=k` 的含义、为什么叫 invariant;手续费如何进入储备并影响 `k`  
- 看完能回答:  
  - swap 发生时,系统状态变量怎么变?  
  - 哪些规则必须守住?  
- 参考:https://docs.uniswap.org/contracts/v2/concepts/protocol-overview/how-uniswap-works

2) **Uniswap v2:Swaps(兑换机制)**  
- 看什么:用户视角的“给定输入→得到输出”的解释  
- 看完能回答:  
  - 为什么我们的仿真器可以用 input-driven 的 `swap(dx)` 来建模(即使真实合约接口更复杂)?  
- 参考:https://docs.uniswap.org/contracts/v2/concepts/core-concepts/swaps

3) **Uniswap v2:Fees(手续费)**  
- 看什么:0.3% fee 的经济含义;手续费如何留在池子里并让 LP token 更值钱  
- 看完能回答:  
  - fee 在我们的模型里该怎么体现?  
  - 怎么用测试抓出 fee 写反/写错/重复扣?  
- 参考:https://docs.uniswap.org/contracts/v2/concepts/advanced-topics/fees

4) **Uniswap v2:Pricing(定价原理)**  
- 看什么:价格如何由储备与规则决定;为什么买走一种资产会更“贵”(滑点)  
- 看完能回答:  
  - 为什么大单的单位成交价更差(滑点单调性)?  
  - 这件事应该如何写成一个“性质测试”?  
- 参考:https://docs.uniswap.org/contracts/v2/concepts/advanced-topics/pricing

5) **Uniswap v2:Common Errors(常见错误,尤其 UniswapV2: K)**  
- 看什么:`K` 错误意味着什么;为什么“违反约束”会被系统拒绝  
- 看完能回答:  
  - 如果仿真里出现“K 类错误”,意味着我破坏了什么规则/记账自洽?  
- 参考:https://docs.uniswap.org/contracts/v2/reference/smart-contracts/common-errors

6) **Uniswap v2 Core Whitepaper(白皮书 PDF,节选阅读)**  
- 建议读法:不需要全读  
  - 先读:整体介绍、pair 与储备/份额关系、手续费与风险面  
- 看完能回答:  
  - 我们在项目 1 的建模边界是什么?哪些细节可以合理简化而不改变关键机制?  
- 参考:https://app.uniswap.org/whitepaper.pdf

---

# B. 验证与可复现(必须看:把“不变量”变成自动验收)

> 目标:看完能写出并跑通 `tests/test_invariants.py`,并理解失败信息;能保证固定 seed 可复现。

7) **pytest:Get Started(入门)**  
- 看什么:如何创建第一个测试、如何运行测试、如何读懂失败信息  
- 看完能做到:  
  - 能跑通 `tests/test_invariants.py`  
  - 能读懂红灯提示,知道是哪条规则没守住  
- 参考:https://docs.pytest.org/en/stable/getting-started.html

8) **pytest:Assertions(断言与失败信息)**  
- 看什么:pytest 如何增强 assert 的失败输出(新手排错非常关键)  
- 看完能做到:  
  - 能根据失败信息定位“是哪条不变量没守住”  
- 参考:https://docs.pytest.org/en/stable/how-to/assert.html

9) **pytest:Fixtures(复用初始化/固定 seed)**  
- 看什么:fixtures 的作用(统一初始化、减少重复 setup)  
- 看完能做到:  
  - 把“固定初始池子状态 / 固定 seed / 固定输入脚本”做成 fixture  
- 参考:https://docs.pytest.org/en/stable/how-to/fixtures.html

10) **Python random:可复现说明(seed)**  
- 看什么:为什么 seed 能复现伪随机序列;复现时需要注意版本/环境  
- 看完能回答:  
  - 为什么我们必须固定 seed?为什么还要记录 Python 版本?  
- 参考:https://docs.python.org/3/library/random.html

11) **GitHub Actions:Building and testing Python(CI 自动跑测试)**  
- 看什么:如何在 CI 中安装依赖、运行 pytest  
- 看完能回答:  
  - 为什么课程要 CI 门禁?CI 如何保证可验收、可复现?  
- 参考:https://docs.github.com/actions/guides/building-and-testing-python

---

# C. 实验输出与证据链(必须看:产出 metrics.csv + figures)

> 目标:看完能把每个 scenario/seed 的指标写到一张表,并一键生成至少两张图。

12) **pandas:读写 CSV(metrics.csv)**  
- 看什么:`read_csv` / `to_csv` 的最基础用法  
- 看完能做到:  
  - 把每次运行的关键指标写入 `results/metrics.csv`  
- 参考:https://pandas.pydata.org/docs/getting_started/intro_tutorials/02_read_write.html

13) **matplotlib:最基本画图 + savefig**  
- 看什么:画曲线图、保存为文件  
- 看完能做到:  
  - 生成至少两张图(例如 price 曲线、k 或偏离曲线)并保存到 `results/figures/`  
- 参考:https://matplotlib.org/stable/gallery/lines_bars_and_markers/simple_plot.html

---

# D. 强烈建议读 / 选读(不影响及格,但会更轻松、更深入)

## D1. 强烈建议(零基础更快建立直觉)
14) **Uniswap v2 Explained(Beginner Friendly)**  
- 作用:用更直观的方式理解 pool/LP/swap/fee  
- 看完能回答:  
  - 池子到底是什么?LP 为什么能赚手续费?  
- 参考:https://flow.com/engineering-blogs/uniswap-v2-explained-beginner-friendly

## D2. 选读(看真实源码结构即可)
15) **Uniswap v2-core GitHub 仓库(合约源码)**  
- 只建议:看结构、看命名,不要钻 Solidity 细节  
- 适合:想理解“真实协议接口 vs 教学仿真 API”差异的同学  
- 参考:https://github.com/Uniswap/v2-core

## D3. 选读(更强的不变量测试:自动找边界)
16) **Hypothesis(Property-based Testing)**  
- 作用:自动生成大量边界输入,更容易发现你没想到的极端 bug  
- 适合:pytest 已熟练,想把不变量测试做得更强的同学  
- 参考:https://hypothesis.readthedocs.io/

## D4. 后续项目预告(项目 1 不要求)
17) **SALib Basics(敏感性分析:项目 2/3 才会用)**  
- 参考:https://salib.readthedocs.io/en/latest/user_guide/basics.html

18) **Mesa First Model(ABM:项目 4 才会用)**  
- 参考:https://mesa.readthedocs.io/latest/tutorials/0_first_model.html

---

## 最短阅读路线(时间紧就按这个来)
- **只想按时交付项目 1**:A1–A6 + B7–B11 + C12–C13  
- **完全零基础怕看不懂**:先读 D1,再回到 A 组  
- **想冲高分**:选读 D2 / D3

---