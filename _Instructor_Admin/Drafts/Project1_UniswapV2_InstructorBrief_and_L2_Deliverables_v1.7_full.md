# 项目 1（第 1–2 周）：Uniswap v2 协议建模与仿真（Protocol as System）
> **交付形态：** Verification-first（先把不变量测试写对）+ 可复现（固定 seed）+ 可自动验收（CI 输出 `grade.json`）  
> **适用人群：** 专业学位硕士（普遍无 DeFi/合约/编程基础）  
> **项目目标：** 把“协议”翻译成 **状态机（State Machine）+ 硬规则（Invariants）+ 外部输入（Scenario Inputs）**，并用仿真与测试证明机制正确与系统脆弱点。

---

## 你要讲什么（Instructor Brief 的核心）

### 0) 先用 2 分钟建立共同语言（给零基础同学）
把 Uniswap v2 想成一个“自动换汇机”：

- 里面有两个“库存”（两种资产的储备）：`x` 和 `y`
- 你投进去一些 `x`，机器吐给你一些 `y`
- 它的定价规则不是人工报价，而是一条简单的曲线约束：常见写法是 **`x * y = k`**
  - **无手续费（fee=0）时：** swap 前后 `k` 近似保持不变（允许数值误差）
  - **有手续费（fee>0）时：** 手续费留在池子里，swap 后 `k` 通常 **非下降**（这是 LP 获益的重要来源之一）
- 任何人也可以把两种资产**按池子比例**存进去成为 LP（流动性提供者），拿到“份额凭证”（pool token），代表你对库存的按比例所有权（真实 Uniswap v2 中，router 会尽量让存入比例贴近池子比例；若偏离，可能被退回多余部分或等价于向现有 LP“捐赠”，本项目为简化默认按比例存入）。

你要让学生从第一天就把它当作：
> **一个状态机（State Machine） + 一组硬规则（Invariants） + 一堆外部输入（Scenario Inputs）。**

---

### 1) 系统边界与状态变量

#### 1.1 系统边界（你要明确“我们不模拟什么”）
为了两周内**可交付、可验收、可复现**，项目 1 建议把边界锁死到“一个池子、三类事件”。

**我们模拟（In-scope）**
- **一个交易对池子（Pair/Pool）**：只有两种资产储备 `reserve_x, reserve_y`
- **Swap（兑换）**：`x -> y` / `y -> x`（核心）
- **Add/Remove Liquidity（可选加分项）**：存入/取出流动性，产生/销毁 LP 份额（做最简版即可）
- **Fee（手续费）**：每次 swap 有手续费，手续费**留在池子里**，价值归 LP（用最简方式表达即可）

> **交付层级建议（非常重要，避免两周做不完）**  
> - **Pass（必做）**：Swap（双向）+ Fee + Invariants/tests + Scenarios + Outputs/复现  
> - **Excellent（加分）**：再做最简 LP（add/remove + shares）

**我们不模拟（Out-of-scope）**
- 链上环境：区块、Gas、MEV、路由、多跳交易、真实合约细节
- 真实用户行为：策略博弈、套利机器人（项目 1 不做对抗/多 Agent）
- 真实市场预测：只做“压力测试式情景”，不做“拟合真实数据”

用工程语言讲原因：
> **“先把系统边界固定，才能写出可验证的合同（tests）。否则你永远不知道 bug 来自协议，还是来自你加的复杂世界。”**

#### 1.2 状态变量（State Variables）：把协议翻译成系统状态
把状态变量分成 3 层（对零基础非常友好）：

**A. 协议核心状态（必需）**
- `x = reserve_x`：池子里 Token X 的库存
- `y = reserve_y`：池子里 Token Y 的库存
- `fee_rate`：手续费比例（例如 `0.003`）
- `k = x * y`：乘积（**派生指标**：用于检查约束/观察变化；`fee>0` 时通常非下降）

> 对学生说清楚：  
> **状态变量不是“指标”，它是系统下一步行为的输入。库存变了，下一笔交易价格就变了。**

**B. 派生状态（Derived，建议有）**
- `price_mid = y / x`：池内“中间价/观察价”（**只用于观察**，不等于成交价）
- 成交价请看：`trade_price = dy/dx`（会受到滑点与 fee 影响）
- `spot_slope`（可选）：曲线局部斜率（高级，不必强制）

**C. LP 与费用状态（项目 1：做“最简计账”，不追求完全真实）**
- `lp_total_shares`：LP 份额总量（pool token 总量）
- `lp_shares[user]`：某个 LP 的份额（可以只做一个 LP 代表即可）
- `fee_accum_x / fee_accum_y`（可选）：累计留在池子里的手续费  
  - 或者不单独记账：只要 swap 的状态更新正确（输入全量入池、成交用有效输入），即可从储备与 `k` 的变化推断 fee 效应

你讲解时建议配一张“状态—事件—更新”表（极其有用）：

| 事件 | 输入 | 更新哪些状态 | 你希望学生立刻想到的硬规则 |
|---|---|---|---|
| swap x→y | `dx` | `x↑, y↓, k 变化` | 储备非负；输出不超库存；fee>0 输出更小；`k`（fee>0）非下降 |
| swap y→x | `dy` | `y↑, x↓, k 变化` | 同上（方向对称） |
| add/remove（可选） | `ax, ay` 或 `shares` | `x,y,lp_shares` | 份额守恒/按比例索取权（最简版即可） |

---

### 2) 不变量（Invariants）与守恒测试

#### 2.1 不变量的工程定义
- **不变量（Invariant）**指协议在任何合法输入与任何执行路径下都必须满足的硬约束：一旦被违反，要么实现存在 bug，要么数值过程失控。
- 在工程实现中，不变量不是“写在文档里的正确性宣言”，而应被**形式化为断言（assertions）**并固化为**单元测试/性质测试（tests）**。
- 因此，项目 1 的“机制正确”主要由 **tests 的可重复证据**来证明，而不是由文字解释来证明。

> 你可以把 tests 理解为“自动裁判”：跑得快不重要，**跑得符合协议语义**才重要。

#### 2.2 项目 1 最低 5 条硬门禁（必做）
> 这 5 条是“安全性 + 合同底线”。任何一条不过，都意味着你的实现尚未达到可验收状态。

1. **I1 储备非负（Safety）**  
   - 断言：任意事件后 `x >= 0` 且 `y >= 0`（允许 `-eps` 级别的浮点误差）。  
   - 典型失败信号：状态更新方向/符号错误，或输出计算导致库存被扣成负数。

2. **I2 输出有界 / No-drain（Safety）**  
   - 断言：对 `x→y`，`0 <= dy <= y_before`；对 `y→x`，`0 <= dx <= x_before`。  
   - 典型失败信号：`get_amount_out` 公式或参数顺序（`reserve_in/reserve_out`）错误；极端输入未处理。

3. **I3 边界行为 sanity（Boundary, 教学 API）**  
   - 断言：`dx=0 => dy=0` 且 `(x_new,y_new)=(x,y)`；同理 `dy=0`。  
   - 典型失败信号：无输入仍更新状态、除零/NaN、或边界条件未覆盖。

4. **I4 手续费一致性（Fee semantics）**  
   - 断言：同状态同输入下，`amount_out(fee>0) <= amount_out(fee=0)`（两方向都测）。  
   - 典型失败信号：手续费方向加反（把 fee 当成折扣），或 fee 被错误地从储备中扣除。

5. **I5 可复现（Reproducibility）**  
   - 断言：固定 seed 或固定交易脚本（trade tape）重复运行，关键结果一致（或在 eps 容差内一致）。  
   - 典型失败信号：随机数未被控制、隐式依赖时间/全局状态、或流程存在非确定性分支。

#### 2.3 建议一并作为必做的 3 条性质测试（低成本，高价值）
> 这 3 条用于“钉死曲线与费用语义”，能显著降低“看似能跑、但机制不对”的风险。

6. **I6 滑点单调性（Curve shape sanity）**  
   - 断言：在同一状态下，大单的平均成交价更差：`dy_large/dx_large <= dy_small/dx_small`。  
   - 典型失败信号：输出公式形状不对（不是 constant-product 曲线），或分母/参数顺序写错。

7. **I7 Constant product 下界（Curve correctness）**  
   - 语义：  
     - `fee=0` 时，swap 前后 `k=x*y` 应近似恒定（允许数值误差）；  
     - `fee>0` 时，手续费留在池子里，swap 后 `k` 应满足 `k_after >= k_before - eps`。  
   - 典型失败信号：费率处理或状态更新错误，导致 `k` 异常下降或跳变。

8. **I8 状态更新一致性（Fee stays in pool）**  
   - 语义：成交计算可以使用有效输入（`dx_eff = dx*(1-fee)`），但**状态更新必须使用全量输入**，因为手续费“留在池子里”。  
   - 断言：  
     - `x→y`：`x_new = x + dx`，`y_new = y - dy`  
     - `y→x`：`y_new = y + dy_in`，`x_new = x - dx_out`  
   - 典型失败信号：把 `dx_eff` 作为入池量（手续费没有留在池子里），或 reserve 更新方向写反。

> **关于 eps / 浮点误差**：建议统一设定 `epsilon`（例如 `1e-12`），并对 “≈” 的比较使用 `math.isclose` 或一致的容差策略。



### 3) 随机性与情景：把外部输入建模成可复现的压力测试

#### 3.1 随机性的目的
不是预测市场，而是**压力测试**：不同输入压力方向下是否稳定、是否违反不变量、哪里最脆弱。

#### 3.2 项目 1 的“降维情景法”（可复现的压力测试输入）
本项目不要求 GBM/Poisson/Pareto 等复杂过程。你只需要把“外部订单流”降维成四类可控输入，并保证可复现：

- **交易方向（direction）**：随机或轻微偏置（`direction_bias`）  
  - `direction_bias=0.5` 表示两方向对称；大于 0.5 表示更偏 `x→y`。  
  - **课程建议默认 0.5**（对称），除非你在 memo 里明确说明你要研究方向偏置的影响。
- **交易规模（size）**：从 3 档离散档位（small/medium/large）抽样（`size_levels`）
- **交易频率（frequency）**：每步发生交易的概率（`trade_probability`）
- **冲击（shock）**：指定某一步发生“异常大”的单笔交易（尾部事件），并允许方向可变（`shock.*`）

> 重要：本项目的三维覆盖（流动性 L / 强度 I / 冲击 S）是“压力大小”的分类；  
> `direction_bias` 属于“压力方向性”的额外维度，默认保持对称以便不同情景可比。



#### 3.3 情景覆盖要求（可验收版：定义清晰、结果可比）
你必须提供**至少 6 个 scenarios**。为保证可比性与自动验收，本项目采用以下约定：

**三维定义（操作性定义）**
- **流动性（L, Liquidity）**：用初始储备规模定义（曲线深度）。  
  - High L：`init_reserves` 大（例如 `[100000, 100000]`）  
  - Low L：`init_reserves` 小（例如 `[10000, 10000]`）
- **交易强度（I, Intensity）**：用“频率 × 规模”的综合压力定义。  
  - frequency：`trade_probability`  
  - size：`size_levels`（3 档离散量级）  
  - 课程约定：Low/High 强度由 **`trade_probability` 与 `size_levels` 共同刻画**（两者在同一强度标签下保持一致）。
- **冲击（S, Shock）**：指定时刻的尾部事件（异常大单）。  
  - NoShock：`shock.enabled=false`  
  - WithShock：`shock.enabled=true` 且包含 `at_step/size_multiplier/direction`

**覆盖要求（最小但信息量最高）**
- 你必须覆盖 **2×2 的无冲击基底**（4 个场景）：High/Low × Low/High × NoShock  
- 并在其中选取 **至少 2 个代表性象限**加入冲击（WithShock），且冲击方向必须覆盖一次 `x_for_y` 与一次 `y_for_x`（避免把脆弱性误归因到某个 token）。

对应 6 个情景（命名可不同，但语义必须一致）：

| Scenario | 初始流动性 | 交易强度 | 冲击 |
|---|---|---|---|
| S1 | High | Low | NoShock |
| S2 | High | High | NoShock |
| S3 | Low | Low | NoShock |
| S4 | Low | High | NoShock |
| S5 | High | Low | WithShock（x→y） |
| S6 | Low | High | WithShock（y→x） |

**参数必须遵守以下约束**（为保证可比性与复现）：
- `steps`：所有 scenarios 必须相同（建议 2000）
- `fee_rate`：所有 scenarios 必须相同（建议 0.003）
- `direction_bias`：默认 0.5（对称），除非你在 memo 中明确解释偏置研究目的
- `trade_probability`：Low 强度建议 0.3；High 强度建议 0.9（可在 ±0.1 内微调，但同一强度标签下保持一致）
- `size_levels`：必须为 3 档离散值（small/medium/large）；为保证可比性：  
  - **同一象限及其 shock 变体保持一致**（例如 `S1` 与 `S5` 的 `trade_probability/size_levels` 应一致；`S4` 与 `S6` 一致）。
- `shock`：WithShock 场景必须包含 `at_step`、`size_multiplier`、`direction`，且方向覆盖 `x_for_y` 与 `y_for_x`

**每个 scenario 必须输出以下最小证据字段**（写入 `results/metrics.csv`）：
- `scenario_name, seed, invariant_violations, min_reserve_x, min_reserve_y, nan_inf_count, avg_price_mid, fee_rate`
- 以及至少两张图：`price_mid_timeseries` 与 `k_timeseries`



---

### 4) Verification 优先于做大：完成定义（Definition of Done）
项目 1 结束时必须“全绿”：

- tests：≥5（建议 8：I1–I8）全通过
- scenarios：≥6 个情景一键跑通
- reproducibility：固定 seed 可复现
- outputs：自动生成 `results/metrics.csv` + `results/figures/`（至少 2 张图）
- README 一页 memo：回答“最脆弱/最稳情景是什么”，并指向证据文件（metrics/figures/tests）
  - **判据**以：不变量违例、数值崩溃（NaN/Inf）、储备接近枯竭为主  
  - **价格偏移**是输入造成的自然结果，不视为协议错误（因为本项目不含套利/价格锚）

---

# 第二层交付（L2 Deliverables：直接落到 starter repo 的“可验收合同”）

> 建议将下列三份文件作为 starter repo 的强制合同：学生只需补齐即可。

---

## 1) `spec.yaml`（机器可读规格书）
保存为：`spec.yaml`

```yaml
meta:
  course: "Agentic Protocol Modeling & Simulation Studio"
  project: "P1 Protocol as System — Uniswap v2 AMM"
  version: "v1.6"
  student: "<your_name>"
  repo: "<your_repo_url>"

decision:
  question: >
    在不同外部情景输入下（流动性薄/厚、交易强度高/低、是否存在冲击），
    Uniswap v2 风格 AMM 的机制是否稳定？哪些情景最脆弱、哪些最稳？
  memo: "README.md (one-page memo with evidence pointers)"

scope:
  in_scope:
    - "Single pool reserves x,y"
    - "Swap x->y and y->x (teaching API: input-driven)"
    - "Fee model (fee stays in pool, affects pricing)"
    - "Scenario-driven stress tests (synthetic)"
    - "Optional: minimal add/remove liquidity with LP shares (bonus)"
  out_of_scope:
    - "Onchain details: gas, blocks, routing, MEV"
    - "Arbitrage/multi-agent dynamics (not required in P1)"
    - "Historical fitting (no need in P1)"

state_variables:
  required: ["reserve_x", "reserve_y", "fee_rate", "k"]
  recommended: ["price_mid", "trade_price"]
  optional: ["lp_total_shares", "lp_shares_single_provider", "fee_accum_x", "fee_accum_y"]

protocol_model:
  name: "UniswapV2-like Constant Product AMM"
  fee_rate_default: 0.003
  pricing_convention: >
    Teaching convention:
    - amount_out uses effective input: amount_in_eff = amount_in*(1-fee)
    - state update adds full amount_in to reserve_in (fee stays in pool),
      reserve_out decreases by amount_out.
    k semantics:
    - fee=0: k approximately constant after swaps (within eps)
    - fee>0: k should be non-decreasing (within eps)
  numeric:
    number_type: "float"
    epsilon: 1e-12

randomness_and_scenarios:
  scenarios_file: "experiments/scenarios.yaml"
  seeds: [0, 1, 2, 3, 4]
  randomness_policy: "direction coin flip + discrete size levels + optional shock"

verification_plan:
  tests_required_min: 5
  tests_required:
    - "I1 reserves non-negative"
    - "I2 output bounded (no drain)"
    - "I3 zero-input boundary sanity"
    - "I4 fee monotonic sanity"
    - "I5 reproducibility"
  tests_recommended:
    - "I6 slippage monotonicity"
    - "I7 constant product lower bound"
    - "I8 state update consistency (fee stays in pool)"

outputs:
  metrics_csv: "results/metrics.csv"
  figures_dir: "results/figures/"
  min_figures: ["price_mid_timeseries", "k_timeseries"]
  min_metrics: ["invariant_violations", "min_reserve_x", "min_reserve_y", "nan_inf_count", "avg_price_mid", "fee_rate"]
```

---

## 2) `experiments/scenarios.yaml`（6 个标准情景）
保存为：`experiments/scenarios.yaml`

```yaml
base:
  fee_rate: 0.003
  steps: 2000
  trade_probability: 0.6
  direction_bias: 0.5          # 0.5 = 对称；>0.5 更偏 x->y
  size_levels: [10, 50, 200]   # small/medium/large（离散档位，便于复现）
  shock:
    enabled: false
    at_step: 1000
    size_multiplier: 20
    direction: "x_for_y"

scenarios:
  - name: S1_highL_lowI_noShock
    init_reserves: [100000, 100000]
    trade_probability: 0.3
    size_levels: [10, 30, 80]
    shock: { enabled: false }

  - name: S2_highL_highI_noShock
    init_reserves: [100000, 100000]
    trade_probability: 0.9
    size_levels: [30, 100, 300]
    shock: { enabled: false }

  - name: S3_lowL_lowI_noShock
    init_reserves: [10000, 10000]
    trade_probability: 0.3
    size_levels: [5, 20, 50]
    shock: { enabled: false }

  - name: S4_lowL_highI_noShock
    init_reserves: [10000, 10000]
    trade_probability: 0.9
    size_levels: [20, 80, 250]
    shock: { enabled: false }

  - name: S5_highL_lowI_withShock
    init_reserves: [100000, 100000]
    trade_probability: 0.3
    size_levels: [10, 30, 80]
    shock:
      enabled: true
      at_step: 1000
      size_multiplier: 30
      direction: "x_for_y"

  - name: S6_lowL_highI_withShock
    init_reserves: [10000, 10000]
    trade_probability: 0.9
    size_levels: [20, 80, 250]
    shock:
      enabled: true
      at_step: 600
      size_multiplier: 40
      direction: "y_for_x"
```

---

## 3) `tests/test_invariants.py`（测试合同：双向 swap + 曲线核心 + fee 留池）
保存为：`tests/test_invariants.py`

```python
import math
import pytest

EPS = 1e-12

from src.simulator import get_amount_out, swap_x_for_y, swap_y_for_x


def approx_leq(a: float, b: float, eps: float = EPS) -> bool:
    return a <= b + eps


def approx_geq(a: float, b: float, eps: float = EPS) -> bool:
    return a + eps >= b


def approx_eq(a: float, b: float, eps: float = EPS) -> bool:
    return abs(a - b) <= eps


def approx_close(a: float, b: float, rel: float = 1e-12, abs_tol: float = 1e-8) -> bool:
    return math.isclose(a, b, rel_tol=rel, abs_tol=abs_tol)


# I1: 储备非负（两方向）
def test_I1_reserves_non_negative_both_directions():
    x, y = 10_000.0, 10_000.0
    fee = 0.003
    tape = [1.0, 5.0, 10.0, 50.0, 100.0] * 20

    for a in tape:
        dy, x, y = swap_x_for_y(a, x, y, fee)
        assert x >= -EPS
        assert y >= -EPS
        assert dy >= -EPS

        dx, x, y = swap_y_for_x(a, x, y, fee)
        assert x >= -EPS
        assert y >= -EPS
        assert dx >= -EPS


# I2: 输出有界（no-drain，方向对称）
def test_I2_output_bounded_both_directions():
    x, y = 10_000.0, 10_000.0
    fee = 0.003

    for dx_in in [0.0, 1.0, 10.0, 1_000.0, 1_000_000.0]:
        dy_out = get_amount_out(dx_in, x, y, fee)
        assert dy_out >= -EPS
        assert dy_out <= y + EPS

    for dy_in in [0.0, 1.0, 10.0, 1_000.0, 1_000_000.0]:
        dx_out = get_amount_out(dy_in, y, x, fee)
        assert dx_out >= -EPS
        assert dx_out <= x + EPS


# I3: 0 输入边界 sanity（教学 API）
def test_I3_zero_input_no_state_change_both_directions():
    x0, y0 = 10_000.0, 10_000.0
    fee = 0.003

    dy, x1, y1 = swap_x_for_y(0.0, x0, y0, fee)
    assert approx_eq(dy, 0.0)
    assert approx_eq(x1, x0)
    assert approx_eq(y1, y0)

    dx, x2, y2 = swap_y_for_x(0.0, x0, y0, fee)
    assert approx_eq(dx, 0.0)
    assert approx_eq(x2, x0)
    assert approx_eq(y2, y0)


# I4: fee 单调一致性（fee>0 输出更小，方向对称）
def test_I4_fee_monotonic_sanity_both_directions():
    x, y = 100_000.0, 100_000.0
    fee = 0.003

    dx_in = 1_000.0
    dy_fee0 = get_amount_out(dx_in, x, y, fee_rate=0.0)
    dy_fee = get_amount_out(dx_in, x, y, fee_rate=fee)
    assert approx_leq(dy_fee, dy_fee0)

    dy_in = 1_000.0
    dx_fee0 = get_amount_out(dy_in, y, x, fee_rate=0.0)
    dx_fee = get_amount_out(dy_in, y, x, fee_rate=fee)
    assert approx_leq(dx_fee, dx_fee0)


# I5: 可复现（同输入脚本）
def test_I5_reproducibility_same_trade_tape():
    fee = 0.003
    x0, y0 = 50_000.0, 50_000.0
    tape = [("x_for_y", 10.0), ("x_for_y", 20.0), ("y_for_x", 5.0), ("y_for_x", 50.0)] * 50

    def run_once():
        x, y = x0, y0
        for direction, amount_in in tape:
            if direction == "x_for_y":
                _, x, y = swap_x_for_y(amount_in, x, y, fee)
            else:
                _, x, y = swap_y_for_x(amount_in, x, y, fee)
        return x, y

    xA, yA = run_once()
    xB, yB = run_once()
    assert approx_eq(xA, xB)
    assert approx_eq(yA, yB)


# I6: 滑点单调性（大单平均成交价更差）
def test_I6_slippage_monotonicity():
    x, y = 100_000.0, 100_000.0
    fee = 0.003

    dx_small = 100.0
    dx_large = 5_000.0

    dy_small = get_amount_out(dx_small, x, y, fee)
    dy_large = get_amount_out(dx_large, x, y, fee)

    assert approx_leq(dy_large / dx_large, dy_small / dx_small)


# I7: constant product 下界（曲线核心）
def test_I7_constant_product_lower_bound():
    x0, y0 = 100_000.0, 100_000.0
    dx_in = 1_234.0
    dy_in = 2_345.0

    # fee=0 => k 近似恒定
    for direction in ["x_for_y", "y_for_x"]:
        x, y = x0, y0
        k0 = x * y
        if direction == "x_for_y":
            _, x, y = swap_x_for_y(dx_in, x, y, fee_rate=0.0)
        else:
            _, x, y = swap_y_for_x(dy_in, x, y, fee_rate=0.0)
        k1 = x * y
        assert approx_close(k1, k0, rel=1e-12, abs_tol=1e-6)

    # fee>0 => k 非下降
    fee = 0.003
    for direction in ["x_for_y", "y_for_x"]:
        x, y = x0, y0
        k0 = x * y
        if direction == "x_for_y":
            _, x, y = swap_x_for_y(dx_in, x, y, fee_rate=fee)
        else:
            _, x, y = swap_y_for_x(dy_in, x, y, fee_rate=fee)
        k1 = x * y
        assert approx_geq(k1, k0, eps=1e-6)


# I8: 状态更新一致性（手续费留池：输入全量入池）
def test_I8_state_update_consistency_fee_stays_in_pool():
    x0, y0 = 100_000.0, 100_000.0
    fee = 0.003

    dx_in = 1_000.0
    dy_out, x1, y1 = swap_x_for_y(dx_in, x0, y0, fee)
    assert approx_close(x1, x0 + dx_in, abs_tol=1e-9)
    assert approx_close(y1, y0 - dy_out, abs_tol=1e-9)

    dy_in = 1_000.0
    dx_out, x2, y2 = swap_y_for_x(dy_in, x0, y0, fee)
    assert approx_close(y2, y0 + dy_in, abs_tol=1e-9)
    assert approx_close(x2, x0 - dx_out, abs_tol=1e-9)
```

---

## 最小接口提示（放在 starter repo，避免新手卡住）
为了让 tests 直接运行，你的 `src/simulator.py` 至少提供三个函数签名：

实现时请使用标准的 constant-product 输出公式（与 Uniswap v2 路由常用 `getAmountOut` 等价）：
- `amount_in_eff = amount_in * (1 - fee_rate)`
- `amount_out = (amount_in_eff * reserve_out) / (reserve_in + amount_in_eff)`

- `get_amount_out(amount_in, reserve_in, reserve_out, fee_rate) -> amount_out`
- `swap_x_for_y(dx_in, x, y, fee_rate) -> (dy_out, x_new, y_new)`
- `swap_y_for_x(dy_in, x, y, fee_rate) -> (dx_out, x_new, y_new)`

---

## 推荐运行顺序（写在 README 顶部）
```bash
pytest -q
python -m experiments.run_all --scenarios experiments/scenarios.yaml --seeds 0 1 2 3 4
```

> 排障优先级：先 tests 全绿 → 再 scenarios 能跑 → 再 metrics → 最后 figures 美化

---

## 5) 项目 1 工具与工作流（Tooling & Workflow）

> 目标：让零基础同学在 **30 分钟内**完成“能跑 tests、能跑 scenarios、能生成 outputs”的闭环。  
> 本项目只使用主线工具：**Python + pytest + pandas/matplotlib**。  
> 其它工具（SALib/Mesa/SimPy/PySD）属于后续项目或选修支线，本项目不要求。

### 5.1 你需要的最小工具栈
- Python 3.10+（推荐 3.11）
- 包管理：`pip`
- 测试：`pytest`
- 数据与画图：`pandas`, `matplotlib`
-（可选但推荐）格式化：`ruff`（或 `black`），用于统一风格、减少低级错误

### 5.2 项目 1 的 repo 合同（你必须按这个结构放文件）
```text
.
├── src/
│   └── simulator.py                # 核心：swap/get_amount_out 等
├── tests/
│   └── test_invariants.py          # I1–I8（至少 I1–I5）
├── experiments/
│   ├── scenarios.yaml              # 6 个情景（2×2×2 覆盖）
│   └── run_all.py                  # 批量运行 + 产出 metrics/figures
├── results/
│   ├── metrics.csv                 # 机器可读证据
│   └── figures/                    # 至少两张图：price_mid、k
├── spec.yaml                       # 机器可读规格书（决策问题+验证计划）
├── README.md                       # 一页 memo：结论 + 指向证据文件
└── requirements.txt                # 依赖（便于 CI）
```

### 5.3 一键运行（你要做到这两条命令都能跑）
在项目根目录执行：

```bash
pip install -r requirements.txt
pytest -q
python -m experiments.run_all --scenarios experiments/scenarios.yaml --seeds 0 1 2 3 4
```

运行后你应该看到：
- `pytest` 全绿（至少 I1–I5；建议 I1–I8）
- `results/metrics.csv` 被生成
- `results/figures/` 下至少有两张图（`price_mid_timeseries`, `k_timeseries`）

### 5.4 `requirements.txt`（课程统一依赖，避免环境分裂）
建议课程给一个固定版本范围（避免不同机器“能跑但结果差异巨大”）：

```text
pytest>=7.0
pandas>=2.0
matplotlib>=3.7
pyyaml>=6.0
```

（可选）如果你希望统一风格：
```text
ruff>=0.4
```

### 5.5 你在项目 1 里最常见的 3 个坑（写给零基础同学）
1) **把 `x*y=k` 当作“严格不变”**  
   - `fee=0` 时近似恒定；`fee>0` 时通常非下降（手续费留池）
2) **状态更新把输入写成 `dx_eff`**  
   - 成交计算用 `dx_eff`，但状态更新必须 `x_new=x+dx`（输入全量入池）
3) **只实现一个方向 swap**  
   - 本项目必须 `x->y` 与 `y->x` 都实现，并通过对称测试

### 5.6（可选）CI 自动验收建议（写给助教/你自己）
CI 至少检查三件事：
- `pytest` 必须通过
- `python -m experiments.run_all ...` 必须成功生成 `results/metrics.csv`
- `metrics.csv` 必须包含最小字段（`scenario_name/seed/invariant_violations/...`）

> 这样评分就可以主要靠 `metrics.csv` + tests 证据，而不是靠主观描述。

### 5.7（可选）`grade.json` 的最小约定（如果课程 CI 需要）
- 本项目的核心证据是 **tests + metrics.csv**。若你希望 CI 进一步自动汇总评分，可在流水线最后输出一个 `grade.json`。
- 建议只包含**可机器验证**的信息（不要让模型“主观打分”）。示例：

```json
{
  "tests": {
    "passed": true,
    "passed_count": 8,
    "required_min": 5
  },
  "scenarios": {
    "count": 6,
    "shock_directions": [
      "x_for_y",
      "y_for_x"
    ]
  },
  "artifacts": {
    "metrics_csv": true,
    "figures": [
      "price_mid_timeseries.png",
      "k_timeseries.png"
    ]
  },
  "notes": []
}
```

