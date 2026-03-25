"""
这是你在 Milestone 2 和 3 里要写的回测沙盘引擎器，不要在这里写具体的判断逻辑。
这是你的“实验台”。
"""

import pandas as pd
try:
    from src.simulator import V3Engine
    from src.agent import BaselineAgent, CandidateAgent, AgentVault
except ImportError:
    print("⚠️ 必须先完成 Milestone 1 并把你的引擎和 Agent 代码写好！")
    exit(1)

def run_simulation(agent, csv_data_path):
    print(f"✅ 开始运行代理: {agent.__class__.__name__}")
    # TODO: 编写完整的回测流水线图
    # 1. 挂载环境 V3Engine
    # 2. 读取 CSV，每一行都是一分钟。
    # 3. 每走一分钟，把当前 TICK 抛给 agent.step()。
    # 4. 根据 agent 的反应（HOLD 还是 REBALANCE），去引擎里扣手续费或扣 Gas。
    # 5. 把当前 AgentVault 的持仓快照写到一个 List 里。
    # 6. 用 Matplotlib 全部画出来并输出 CSV 财报。
    pass

if __name__ == "__main__":
    csv_file = "experiments/data/weth_usdc_flash_crash.csv"
    
    vault_base = AgentVault(initial_usdc=10000, initial_eth=0)
    base_agent = BaselineAgent(vault_base)
    
    vault_cand = AgentVault(initial_usdc=10000, initial_eth=0)
    cand_agent = CandidateAgent(vault_cand)
    
    # run_simulation(base_agent, csv_file)
    # run_simulation(cand_agent, csv_file)
    print("Project 2 回测系统未就绪！")
