import sys
import os
import pandas as pd
import pytest

# 路径锁定
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 【修正处 1】：使用你 simulator.py 里真正的类名
from src.simulator import V3PoolStateMachine
from src.agent import CandidateAgent


def test_p1_engine_with_real_historical_data():
    # 【修正处 2】：使用正确的类名和参数名
    engine = V3PoolStateMachine(
        sqrt_price_x96=15840424523315764958611116223,
        liquidity=186401666874945417
    )

    csv_path = os.path.join(project_root, "data", "weth_usdc_flash_crash.csv")
    if not os.path.exists(csv_path):
        pytest.fail(f"🔴 找不到数据文件！请确保文件在: {csv_path}")

    df = pd.read_csv(csv_path)
    agent = CandidateAgent(lower_tick=-200000, upper_tick=-190000)

    rebalance_count = 0
    for index, row in df.iterrows():
        current_tick = row['tick']
        decision = agent.step(current_tick, None)
        if decision.get("action") == "REBALANCE":
            rebalance_count += 1
            print(f">>> 行 {index}: 触发重平衡！")

    assert rebalance_count > 0
    print("\n✅ 恭喜 Fei！测试终于圆满通过了！")


if __name__ == "__main__":
    pytest.main([__file__, "-s"])
