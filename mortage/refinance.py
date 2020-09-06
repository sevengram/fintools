def current_value(future_money, r_inf, n):
  return round(future_money * (1 + r_inf) ** -n, 2)


def term_payment_amount(principal, r_int, m):
  a = (1 + r_int) ** m
  return round(principal * r_int * a / (a - 1), 2)


def term_payment_principal(principal, r_int, n, m):
  p = term_payment_amount(principal, r_int, m)
  return round((p - principal * r_int) * (1 + r_int) ** (n - 1), 2)


def term_payment_interest(principal, r_int, n, m):
  p = term_payment_amount(principal, r_int, m)
  return round(p - (p - principal * r_int) * (1 + r_int) ** (n - 1), 2)


def remaining_balance(principal, r_int, n, m):
  p = term_payment_amount(principal, r_int, m)
  a = (1 + r_int) ** n
  return round(principal * a - p * (a - 1) / r_int, 2)


def total_payment_current_value(principal, r_int, r_inf, m):
  p = term_payment_amount(principal, r_int, m)
  last_term_rb = remaining_balance(principal, r_int, m - 1, m)
  a = (1. + r_inf) ** (1 - m)
  return round(p * (1 - a) * (1. + r_inf) / r_inf + last_term_rb * (
      1. + r_int) * a, 2)


def tax_benefit_current_value(principal, r_int, r_inf, r_tax, m, base):
  p = term_payment_amount(principal, r_int, m)
  value = 0
  for i in range(0, m):
    interest = p - (p - principal * r_int) * (1 + r_int) ** i
    value += max(0, interest - base) * r_tax * (1 + r_inf) ** -i
  return value


if __name__ == '__main__':
  inflation_rate = 2.5 / 100. / 12.

  current_principal = 207370.14
  current_interest_rate = 4.875 / 100. / 12.
  current_terms = 350

  cash_in = 0
  refinance_fee = 5000.00

  new_principal = current_principal - cash_in
  new_interest_rate = 4.375 / 100. / 12.
  new_terms = 360

  tax_rate = 0.20
  standard_deduction = 12000.
  other_deduction = 6000.
  base_deduction = max(standard_deduction - other_deduction, 0) / 12.

  current_term_payment = term_payment_amount(
      current_principal, current_interest_rate, current_terms)
  current_tpcv = total_payment_current_value(
      current_principal, current_interest_rate, inflation_rate, current_terms)
  current_tbcv = tax_benefit_current_value(
      current_principal,
      current_interest_rate,
      inflation_rate,
      tax_rate,
      current_terms,
      base_deduction)

  new_term_payment = term_payment_amount(
      new_principal, new_interest_rate, new_terms)
  new_tpcv = refinance_fee + cash_in + total_payment_current_value(
      new_principal, new_interest_rate, inflation_rate, new_terms)
  new_tbcv = tax_benefit_current_value(
      new_principal,
      new_interest_rate,
      inflation_rate,
      tax_rate,
      new_terms,
      base_deduction)

  print("current_term_payment:", current_term_payment)
  print("current_tpcv:", current_tpcv)
  print("current_tbcv:", current_tbcv)
  print("new_term_payment:", new_term_payment)
  print("new_tpcv:", new_tpcv)
  print("new_tbcv:", new_tbcv)
  print("diff:",
        round((new_tpcv - new_tbcv) - (current_tpcv - current_tbcv), 2))
