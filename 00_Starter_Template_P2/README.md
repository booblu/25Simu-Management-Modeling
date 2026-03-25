# 🤖 Project 2 Starter Sandbox: Active LP Policy

这是你专属的 Project 2 作战实验室。

### 🚨 核心须知：你的引擎在哪里？
本仓库**不再提供 `simulator.py`**！你必须从你的 `Project 1` 仓库中，把你已经通过了极压测试的 `simulator.py` 完整地拷贝到本仓库的 `src/` 目录下。作为首席系统架构师，你需要为你写出来的底层代码负责跨越多个 Project 的生命周期。

### 📂 目录导航
- `src/agent.py`：你需要在这里面编写 `BaselineAgent` 和 `CandidateAgent`。
- `tests/test_milestone_1.py`：里程碑 1，用这里的脚本测试你的 P1 引擎能否消化真实的历史数据并求出正确终值。
- `experiments/run_backtest.py`：在这个文件里把你的 Agent 装载进环境，运行资金曲线回测。
- `experiments/data/weth_usdc_flash_crash.csv`：供你回测使用的真实链上历史交易数据流。
