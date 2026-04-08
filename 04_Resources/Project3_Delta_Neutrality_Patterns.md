# 🧠 Project 3 战术心法包 (Delta Neutrality & LTV Metrics)

> “当你凝视 V3 的无常损失时，对冲引擎也在凝视你。”
> 本文档专门用于指导你如何用严密的代数建立资产负债表（Portfolio），以及如何在程序中计算你借出的那笔高悬着达摩克利斯之剑的“做空负债”。

---

## 🏛️ 秘籍 1：超额抵押与健康因子体系 (The Aave Math)

我们为什么不“直接做空” ETH？因为在去中心化世界，不存在信用借款。你必须先存入稳定资产（如 USDC）当做当铺的抵押物，才能拿走波动性资产（如 ETH）。

在你构建自己的 `aave_mock.py` 时，你必须在里面实现最重要的状态检验函数 `get_health_factor()`。这个数值绝对掌管一切生杀大权。

### 金融断言法则
- **$C$ (Collateral Amount)**: 你存入的美元硬通货（USDC）。价值恒定为 $\$1$。
- **$B$ (Borrow Amount)**: 你借出来的标的币物（本课为 `ETH`）。
- **$P$ (Oracle Price)**: 借入物当下的市场预言机价格。也就是 1 个 ETH 等于几刀 USDC。
- **$LT$ (Liquidation Threshold)**: 清算线阀值系数。例如 `0.8` (80%)，意味着只要你的借款金额超过抵押物总价值的 80%，你就离死不远了。

**你的系统里必须具备的数学内核：**
```python
Total_Collateral_in_USD = C
Total_Debt_in_USD = B * P

# 核心红线计算法则
Health_Factor = (Total_Collateral_in_USD * LT) / Total_Debt_in_USD
```
当你在主脚本每运行一行时间序列，价格 $P$ 发生暴涨时，`Total_Debt_in_USD` 就会变大。
**当 `Health_Factor < 1.0` 的一瞬间：** 
你的所有 $C$ (抵押 USDC) 会瞬间被清算网络没收并化为灰烬（被清算人七折贱卖平仓）。
**在你的 `AaveMock` 中，这个机制是用代码判定的，必须触发系统的归零风暴！**

---

## 🧮 秘籍 2：Delta 对角线抹平法则 (The Hedging Equation)

既然借贷会因为涨价（Price $P$ 上涨）而爆仓，这明明很危险！那我们为什么要借 ETH 出来？
因为我们要在 V3 做市。
如果你拿自己的真钱去买一半的 ETH 和一半的 USDC 放进 Uniswap，如果 ETH 价格 $P$ **暴跌**，你在 Uniswap 的头寸不但不赚钱，反而亏成了废纸。这叫做 **正 Delta 敞口 (Long Bias Delta > 0)**。

于是，华尔街（DeFi Quant）发明了这个玩法：
1. 你先用 10,000 USDC 存进 Aave 引擎（抵押）。
2. 在 Aave 借出价值 `5,000` 美元的 ETH。
3. 把这 `5,000` 美金的借来 ETH 和手里剩下的 `5,000` 美金的 USDC 打包。
4. 放入 V3 引擎做流动性。

### 此时，如果发生了极其绝望的暴跌大灾难：
- 🔴 V3 引擎端：你的 ETH 跌成了废纸，美元损失惨重。
- 🟢 Aave 引擎端：你欠 Aave 的是 ETH！既然 ETH 跌成了废纸，等于你几乎**不用还钱**了（你只需要买一把极其便宜的 ETH 扔回给 Aave 就两清了）。此时，Aave 这头的空单给你赚回了巨额的法币差价！
- **结果：** 完美抵消。你的法币总净值稳如铁板。

### 你的作业难点（Portfolio Manager）：
你需要在主循环中维持一个上帝视角的**联合净值系统**。
在每一个计算 Tick：
```python
# 你的联合资产负债表：
Real_Wealth_USD = P1_V3_Liquid_Value_in_USD + Aave_Collateral_Value_in_USD - Aave_Debt_Cost_in_USD + V3_Fee_Earned_USD
```
如果 `Real_Wealth_USD` 在“5.19 暴跌”中，画出了一条惊艳的直线。
那么你就真正站在了风暴的顶端，做到了跨越协议深渊的风险降维对冲！

**⚠️ 防错警告 (Gotcha)：在真实环境里，Aave 借钱是有年化利息的（Borrow APY）。借出 ETH 不是免费的。在你的 P3 主循环中，别忘了随着时间流逝，不断给自己的 $B$ (Borrow Amount) 里计费滚存复利债务！**
