from enum import Enum

import matplotlib.pyplot as plt
import numpy as np


class OptionType(Enum):
  CALL = 0
  PUT = 1


def compute_profit(option_type, n, premium, strike_price, share_price):
  if option_type == OptionType.CALL:
    delta = share_price - strike_price
  elif option_type == OptionType.PUT:
    delta = strike_price - share_price
  else:
    raise ValueError('Unexpected option type')

  return (max(delta, 0) - premium) * n * 100


if __name__ == '__main__':
  option_type = OptionType.PUT
  strike_price_1 = 116.5
  n_1 = 5
  open_price_1 = 1.03
  close_price_1 = 2.09

  current_profit = (close_price_1 - open_price_1) * n_1 * 100
  strike_price_2 = 114.5
  n_2 = 8
  open_price_2 = 1.05

  price_samples = np.arange(110, 130, 0.25)
  profit_1 = [compute_profit(option_type, n_1, open_price_1,
                             strike_price_1, p) for p in price_samples]
  profit_2 = [current_profit + compute_profit(option_type, n_2, open_price_2,
                                              strike_price_2, p) for p in
              price_samples]
  plt.plot(price_samples, profit_1, 'r-')
  plt.plot(price_samples, profit_2, 'b-')
  plt.show()
