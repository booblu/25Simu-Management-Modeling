import pytest
import pandas as pd
import os

# ⚠️ 注意这里：如果你跑不了这个测试由于找不到 `simulator.py`，因为你还没拷过来。
try:
    from src.simulator import V3Engine
except ImportError:
    V3Engine = None

@pytest.mark.skipif(V3Engine is None, reason="尚未从 P1 移植你的 V3 引擎代码！")
def test_p1_engine_with_real_historical_data():
    """
    Project 2 - Milestone 1: 能不能跑通真实世界的断言
    不要修改预埋价格断言！你的引擎必须能够 100% 精确推导。
    """
    # 真实链上快照初始状态: 
    # 在 2021 年某个区块 ETH/USDC 500 万分比池子
    INITIAL_SQRT_PRICE_X96 = 1999966144503729587422770258286
    
    engine = V3Engine(initial_sqrtPriceX96=INITIAL_SQRT_PRICE_X96)
    
    # 获取同目录下的预埋短路数据 (Mocked for testing)
    csv_path = os.path.join(os.path.dirname(__file__), '../experiments/data/weth_usdc_flash_crash.csv')
    df = pd.read_csv(csv_path)
    
    for index, row in df.iterrows():
        # 这里模拟了每笔真实链上的 Swap 记录输入你的引擎
        engine.execute_swap(
            zeroForOne=bool(row['zeroForOne']),
            amountSpecified=int(row['amountSpecified'])
        )
        
    final_price_x96 = engine.get_sqrtPriceX96()
    
    # 这是我们在链上读取区块状态得到的极其精准的最终截断价格！差 1 wei 都不行。
    # 这里我们随便模拟一个靶标，你实现作业时需要保证匹配。
    TARGET_PRICE_X96 = 2000000000000000000000000000000
    
    print(f"你的引擎最终求导价格: {final_price_x96}")
    assert final_price_x96 == TARGET_PRICE_X96, "你的引擎有运算精度的流失或边界 Bug！"
