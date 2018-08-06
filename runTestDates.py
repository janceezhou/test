# encoding: UTF-8

"""
展示如何执行参数优化。
"""

from __future__ import division


from vnpy.trader.app.ctaStrategy.ctaBacktesting import BacktestingEngine, TICK_DB_NAME, OptimizationSetting


if __name__ == '__main__':
    from vnpy.trader.app.ctaStrategy.strategy.strategyTurtle import TurtleStrategy
    
    # 创建回测引擎
    engine = BacktestingEngine()
    
    # 设置引擎的回测模式为tick
    engine.setBacktestingMode(engine.TICK_MODE)

    # 设置回测用的数据起始日期
    engine.setStartDate('20160601')
    engine.setEndDate('20161231')
    
    # 设置产品相关参数
    engine.setSlippage(0.000001)     # 设置滑点为股指1跳
    engine.setRate(0.0001)      # 设置手续费千1
    engine.setSize(1)           # 设置合约大小 
    engine.setPriceTick(0.000001)   # 设置最小价格变动   
    engine.setCapital(1000)   # 设置回测本金
    
    # 设置使用的历史数据库
    engine.setDatabase(TICK_DB_NAME, 'bitstampUSD')
    
    # 跑优化
    diffDaysSetting = OptimizationSetting()                 # 新建一个优化任务设置对象
    diffDaysSetting.setOptimizeTarget('capital')            # 设置优化排序的目标是策略净盈利
    diffDaysSetting.addParameter('diffDays', 0, 60, 30)    # 增加第一个优化参数atrLength，起始12，结束20，步进2
    
    # 性能测试环境：I7-3770，主频3.4G, 8核心，内存16G，Windows 7 专业版
    # 测试时还跑着一堆其他的程序，性能仅供参考
    import time    
    start = time.time()
    
    # 运行单进程优化函数，自动输出结果，耗时：359秒
    #engine.runOptimization(AtrRsiStrategy, setting)            
    
    # 多进程优化，耗时：89秒
    engine.runParallelTestDates(TurtleStrategy, diffDaysSetting)
    
    print u'耗时：%s' %(time.time()-start)