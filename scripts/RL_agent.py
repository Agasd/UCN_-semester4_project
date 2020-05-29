import pandas as pd
from tensortrade.data import Module, Stream, DataFeed
from tensortrade.exchanges import Exchange
from tensortrade.exchanges.services.execution.simulated import execute_order
from tensortrade.environments import TradingEnvironment
from tensortrade.instruments import USD, BTC, ETH, LTC
from tensortrade.wallets import Portfolio, Wallet
from tensortrade.agents import DQNAgent, A2CAgent
import numpy as np
import quantstats as qs
from sklearn import preprocessing
from tensorflow.keras.models import Sequential, save_model, load_model





def join_data(datasets):
    PATH = "./data/1m_resolution/"
    main_df = pd.DataFrame()
    for dataset in datasets:
        dataset = dataset.split('.csv')[0]
        dataset_file = f'{PATH + dataset}.csv'
        df = pd.read_csv(dataset_file)

        df.rename(columns={"close": f"{dataset}_close", "volume": f"{dataset}_volume"}, inplace=True)

        df.set_index("time", inplace=True)
        df = df[[f"{dataset}_close", f"{dataset}_volume"]]

        if len(main_df) == 0:
            main_df = df
        else:
            main_df = main_df.join(df)

    return main_df


data = join_data(["LTC-USD", "BTC-USD", "ETH-USD"])
data.reset_index(level=0, inplace=True)

data.dropna(inplace=True)

data = data.set_index('time').reindex(np.arange(data['time'].min(), data['time'].max(), 60)) \
    .fillna(np.nan) \
    .reset_index()

data.ffill(inplace=True)
data.set_index("time", inplace=True)

times = sorted(data.index.values)
last_30pct = sorted(data.index.values)[-int(0.3 * len(times))]

data = data[(data.index >= last_30pct)]
buy_data = data.copy()
agent_data = data.copy()

for col in agent_data.columns:
    if col != "target" and col != "future_timestamp" and col != "time":
        agent_data[col] = agent_data[col].pct_change()
        agent_data.dropna(inplace=True)
        print(agent_data.columns)
        print(col)
        agent_data[col] = preprocessing.scale(agent_data[col].values)

data.dropna(inplace=True)

with Module("coinbase") as node_stream:
    nodes = []
    for name in data.columns:
        nodes.append(
            Stream(list(data[name]), name)
        )

data_feed = DataFeed([node_stream])
data_feed.next()
exchange = Exchange("sim-exchange", service=execute_order)(
    Stream(list(data['BTC-USD_close']), "USD-BTC"),
    Stream(list(data['ETH-USD_close']), "USD-ETH"),
    Stream(list(data['LTC-USD_close']), "USD-LTC")

)

portfolio = Portfolio(
    base_instrument=USD,
    wallets=[Wallet(exchange, 100000 * USD),
             Wallet(exchange, 0 * BTC),
             Wallet(exchange, 0 * LTC),
             Wallet(exchange, 0 * ETH)
             ]
)
env = TradingEnvironment(
    feed=data_feed,
    portfolio=portfolio,
    action_scheme='managed-risk',
    reward_scheme='risk-adjusted',
    window_size=20
)
agent = DQNAgent(env)
agent.train(n_steps=300, n_episodes=500)




portfolio.performance.net_worth.plot()

portfolio.performance.plot()


