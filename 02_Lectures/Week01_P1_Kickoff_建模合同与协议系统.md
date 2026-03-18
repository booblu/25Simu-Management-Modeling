# 第 1 周：P1 Kickoff — 建模合同与协议系统

## 1. 本周定位

本周是**项目 1（协议的建模与仿真）**的 Kickoff 周。你将从零建立课程的操作系统（repo 合同、CI 门禁、可验收定义），并把 Uniswap v2 风格的 AMM 理解为**状态机 + 硬规则 + 外部输入**，为第 2 周完成 6 情景与证据链打下基础。

- **所属项目**：P1（第 1–2 周）
- **课堂类型**：Kickoff（发布项目合同 + 讲机制 + 演示骨架）
- **对应总纲**：课程大纲与规划_完整版.md — 第 1 周；**八周讲授单元** 第 1 条（建模合同与可验收性）、第 2 条开头（协议作为动态系统）

---

## 2. 学习目标

- 能说明什么叫“模型做完”：CI 全绿 + 证据链，而非“代码能跑”。
- 能写出 `spec.yaml` 的 v0 版本（决策问题、scope、状态变量、验证计划）。
- 能把 AMM 描述为状态变量（reserve_x, reserve_y, fee_rate, k）+ 事件（swap x→y / y→x）+ 硬规则（储备非负、输出有界、fee>0 时 k 非降）。
- 能在 starter repo 里跑通第一个不变量测试（如 I3 零输入）并触发 CI。
- 能实现 simulator 最小接口：`get_amount_out`, `swap_x_for_y`, `swap_y_for_x`（骨架即可）。

---

## 3. 讲授单元（Instructor Brief）

### 3.1 建模合同与可验收性

**核心概念**  
“模型做完”在这门课里的定义是：**可自动验收**。即通过 CI 门禁（tests 全绿、可复现、产出 metrics/figures），并有一份机器可读的规格书（spec.yaml）和证据指针（README 指向 metrics/figures/tests）。不是“我跑过了就行”，而是“每次 push 都能被同一套规则判定”。

**关键点**  
- Repo 合同：统一目录结构（src/、tests/、experiments/、results/、grade/、.github/workflows/）。  
- CI 至少做两件事：`pytest` 全绿；`python -m experiments.run_all` 成功生成 results/metrics.csv 与 results/figures/。  
- 分数主干由确定性程序产生（grade.py → grade.json）；AI 只做基于证据的解释性点评。

**常见坑**  
- 只在本机跑通、CI 未配置或未通过就认为“做完了”。  
- spec.yaml 与实现脱节（写了的没测、测了的没写进 spec）。

**当周验收标准**  
- spec.yaml v0 已提交；tests/ 下至少有一个不变量测试（建议 I3）且能通过；CI 工作流存在且 pytest 能绿；src/simulator.py 提供三个最小接口且可被 tests 导入。

### 3.2 协议作为动态系统（开头）

**核心概念**  
把 Uniswap v2 想成“自动换汇机”：两个库存（reserve_x, reserve_y）、一条曲线约束（x*y=k）、手续费留池。协议 = **状态机（State Machine）+ 硬规则（Invariants）+ 外部输入（Scenario Inputs）**。

**关键规则**  
- 状态变量：`reserve_x`, `reserve_y`, `fee_rate`, `k = x*y`（派生）。  
- 事件与更新：  
  - swap x→y：输入 dx → x↑, y↓；成交用有效输入 `dx_eff = dx*(1-fee)`，状态更新时**全量 dx 入池**（手续费留池）。  
  - swap y→x：对称。  
- 硬规则：储备非负；输出有界（no-drain）；fee=0 时 k 近似恒定，fee>0 时 k 非降。

**常见坑**  
- 把 `dx_eff` 当作入池量（手续费没有留在池子里）。  
- 只实现一个方向 swap（本项目必须 x→y 与 y→x 都实现并通过对称测试）。

**当周验收标准**  
- 能与教师/同学用“状态—事件—更新—硬规则”表描述 AMM；simulator 实现双向 swap 且通过 I3（零输入边界）。

---

## 4. 现场演示（Live Build）

1. **打开 P1 starter repo**（或课程提供的模板），展示目录结构：`src/simulator.py`, `tests/test_invariants.py`, `experiments/`, `spec.yaml`。
2. **在 `tests/test_invariants.py` 中补全或添加 I3**（零输入边界）：
   - 调用 `swap_x_for_y(0.0, x0, y0, fee)`，断言 `dy==0` 且 `(x_new,y_new)==(x0,y0)`；
   - 同理 `swap_y_for_x(0.0, ...)`。
3. **在 `src/simulator.py` 中实现最小接口**：
   - `get_amount_out(amount_in, reserve_in, reserve_out, fee_rate)`：`amount_in_eff = amount_in*(1-fee_rate)`，`amount_out = (amount_in_eff * reserve_out) / (reserve_in + amount_in_eff)`；
   - `swap_x_for_y(dx_in, x, y, fee_rate)` → `(dy_out, x_new, y_new)`，其中 `x_new = x + dx_in`, `y_new = y - dy_out`；
   - `swap_y_for_x(dy_in, x, y, fee_rate)` → `(dx_out, x_new, y_new)`，对称。
4. **运行**：`pytest -q`，确认 I3 通过；若有 CI，`git push` 后确认 Checks 绿。

**预期结果**：pytest 至少 1 个 test 通过；CI（若已配置）显示绿色。

---

## 5. Studio 任务与检查点

**当堂完成（最小清单）**  
- [ ] 填写或克隆 `spec.yaml` v0（meta、decision.question、scope.in_scope/out_of_scope、state_variables、verification_plan.tests_required_min 与 tests_required）。  
- [ ] 在 `tests/test_invariants.py` 中实现并跑通至少 I3（零输入边界）。  
- [ ] 在 `src/simulator.py` 中实现 `get_amount_out`, `swap_x_for_y`, `swap_y_for_x`，使 I3 通过。  
- [ ] 确认 `pytest -q` 通过；若已配置 CI，当场 push 并确认门禁绿。

**课后（本周内）**  
- [ ] 扩展 tests：至少覆盖 I1（储备非负）、I2（输出有界），建议再补 I4（fee 单调）。目标：第 2 周前达到 I1–I5 全过。  
- [ ] 阅读总纲 3.5 最短路线：A1–A6（协议必读）+ B7–B11（验证与可复现）+ C12–C13（实验输出）。

---

## 6. Show & Ask

**闪电分享主题（3–5 人，每人约 3 分钟）**  
- “我定义的不变量是什么？我打算怎么测？”  
- “我的 spec.yaml 里 scope 和 state_variables 写了什么？”

**公共 Q&A 建议**  
- CI 怎么配？pytest 失败信息怎么读？  
- `get_amount_out` 公式与 Uniswap v2 文档是否一致？  
- 浮点误差用 eps 还是 `math.isclose`？

---

## 7. 阅读与资源

- **必读**：Uniswap v2 — How Uniswap works、Swaps、Fees、Pricing、Common Errors（见 # Project1_readinglist.md 的 A1–A5）；pytest Get Started、Assertions、Fixtures（B7–B9）；Python random 与 seed（B10）。  
- **选读**：Uniswap v2 白皮书节选（A6）；GitHub Actions Building and testing Python（B11）。  
- **参考**：总纲第三节（项目 1 目标、边界、不变量、情景、交付物）。

---

## 8. 交付物与验收

| 交付物 | 说明 |
|--------|------|
| `spec.yaml` | v0：含 meta、decision、scope、state_variables、verification_plan（tests_required_min: 5, tests_required 列表）。 |
| `src/simulator.py` | 至少实现 `get_amount_out`, `swap_x_for_y`, `swap_y_for_x`，与总纲 3.6 最小接口一致。 |
| `tests/test_invariants.py` | 至少 I3 通过；建议已有 I1、I2、I4 骨架。 |
| CI | `.github/workflows/ci.yml` 存在；`pytest` 全绿（门禁）。 |

与总纲 3.6（L2）一致：不要求本周交齐 6 情景与 figures，但 tests 与 simulator 骨架需就绪。

---

## 9. 与总纲的对应关系

| 总纲章节 | 本 MD 覆盖内容 |
|----------|----------------|
| 一、课程定位与目标 | 能力目标体现在“学习目标”与“验收标准”。 |
| 二、四大项目 | P1 第 1 周，Kickoff。 |
| 三、项目 1（3.1–3.6） | 目标与边界、状态与事件、不变量 I1–I8、交付物与 L2。 |
| 七、统一 Repo 结构与自动验收 | 目录结构、CI、门禁。 |
| 八、8 周每周半天安排 | 第 1 周：P1 Kickoff；讲解重点、Studio/交付。 |
| 九、八周讲授单元 | 单元 1（建模合同与可验收性）、单元 2 开头（协议作为动态系统）。 |

---

## 附录：P1 标准 Repo 树（与总纲 7.1 一致）

```
project/
  README.md
  spec.yaml
  src/
    simulator.py
  tests/
    test_invariants.py
  experiments/
    scenarios.yaml
    run_all.py
  results/
    metrics.csv
    figures/
  grade/
    grade.py
    rubric.yaml
    grade.json
  .github/workflows/ci.yml
  requirements.txt
```
