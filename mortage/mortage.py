import matplotlib.pyplot as plt


def future_money_current_value(money, inflation_rate, n):
  return money * (1 + inflation_rate) ** -n


def compute(down_payment, length_of_finance, annual_interest_rate):
  annual_inflation_rate = 0.03
  annual_house_value_increment_rate = 0.031
  annual_investment_return_rate = 0.068

  monthly_inflation_rate = annual_inflation_rate / 12
  monthly_house_value_increment_rate = annual_house_value_increment_rate / 12
  monthly_investment_return_rate = annual_investment_return_rate / 12

  house_price = 290000.0
  current_money = 160000.0
  number_of_months = 360
  monthly_liquid_increment = 2000.0
  current_rental_price = 1400.0
  rental_start_month = 36

  monthly_interest_rate = annual_interest_rate / 12.0
  principal = house_price - down_payment
  t = (1 + monthly_interest_rate) ** length_of_finance
  monthly_payment = principal * monthly_interest_rate * t / (t - 1)
  print("monthly_payment:", monthly_payment)

  total_cost = down_payment
  for i in range(length_of_finance):
    total_cost += future_money_current_value(monthly_payment,
                                             monthly_inflation_rate,
                                             i)
  print("total_cost:", total_cost)

  future_liquid_value = current_money - down_payment
  rental_price = current_rental_price
  for i in range(number_of_months):
    future_liquid_value += monthly_liquid_increment
    if i < length_of_finance:
      future_liquid_value -= monthly_payment
    if future_liquid_value < 0:
      print("Error: liquid value < 0!!")
      exit(0)
    if i >= rental_start_month:
      future_liquid_value += rental_price
    if i % 12 == 0:
      rental_price *= 1 + annual_inflation_rate
    future_liquid_value *= 1 + monthly_investment_return_rate

  liquid_value = future_money_current_value(future_liquid_value,
                                            monthly_inflation_rate,
                                            number_of_months)
  future_house_value = house_price * (1 + monthly_house_value_increment_rate) \
                       ** number_of_months

  house_value = future_money_current_value(future_house_value,
                                           monthly_inflation_rate,
                                           number_of_months)
  print("house_value:", house_value)
  return liquid_value + house_value - total_cost


if __name__ == '__main__':
  length_of_finance = 360
  annual_interest_rate = 0.04625
  down_payment = range(60000, 170000, 10000)
  deltas = [compute(dp, length_of_finance,
                    annual_interest_rate) for dp in down_payment]
  plt.plot(down_payment, deltas, '.r-')

  length_of_finance = 180
  annual_interest_rate = 0.04000
  down_payment = range(60000, 170000, 10000)
  deltas = [compute(dp, length_of_finance,
                    annual_interest_rate) for dp in down_payment]
  plt.plot(down_payment, deltas, '.b-')

  plt.show()
