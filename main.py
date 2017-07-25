from alphavantage.globalstockquotes import GlobalStockQuotes
from alphavantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
#
# ts = TimeSeries(key='92FRTVHCC356S9ZS', output_format='pandas')
# data, meta_data = ts.get_intraday(symbol='GOOG', interval='60min',
#                                   outputsize='full')
# data['close'].plot()
# plt.title('Intraday Times Series for the GOOG stock (1 min)')
# plt.show()

dsq = GlobalStockQuotes(key='92FRTVHCC356S9ZS', output_format='json')
data, meta_data = dsq.get_global_quote(symbol='SOXX')
print(1)