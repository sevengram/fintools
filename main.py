from alphavantage.globalstockquotes import GlobalStockQuotes
from alphavantage.techindicators import TechIndicators
from alphavantage.timeseries import TimeSeries

# ts = TimeSeries(key='92FRTVHCC356S9ZS', output_format='json')
# data, meta_data = ts.get_intraday(symbol='SHA:600839', interval='1min',
#                                   outputsize='full')
# # data['close'].plot()
# # plt.title('Intraday Times Series for the GOOG stock (1 min)')
# # plt.show()

# dsq = GlobalStockQuotes(key='92FRTVHCC356S9ZS', output_format='json')
# data = dsq.get_global_quote(symbol='USO')
# print(data)

td = TechIndicators(key='92FRTVHCC356S9ZS',output_format='json')
data, meta_data = td.get_rsi(symbol='COST')
print(data)