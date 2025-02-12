import backtrader as bt
import pandas as pd

class MovingAverageStrategy(bt.Strategy):
    params = (("short_window", 20), ("long_window", 50))

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(period=self.params.short_window)
        self.sma_long = bt.indicators.SimpleMovingAverage(period=self.params.long_window)

    def next(self):
        if self.sma_short[0] > self.sma_long[0] and not self.position:
            self.buy()
        elif self.sma_short[0] < self.sma_long[0] and self.position:
            self.sell()

def run_backtest(symbol):
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    if "Close" not in df.columns:
        print(f"❌ Erreur : La colonne 'Close' n'existe pas dans {symbol}.csv.")
        return None

    data = bt.feeds.PandasData(dataname=df)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(MovingAverageStrategy)
    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot()

if __name__ == "__main__":
    run_backtest("BTC")
