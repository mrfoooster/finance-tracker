import math


def future_from_present(present_value, i, n):
    return present_value * (1 + i) ** n


def future_from_annual(annual_value, i, n):
    return annual_value * ((1 + i) ** n - 1) / i


def present_from_future(future_value, i, n):
    return future_value * (1 + i) ** (-n)


def present_from_anual(annual_value, i, n):
    return annual_value * ((1 + i) ** n - 1) / (i * (i + 1) ** n)


def annual_from_present(present_value, i, n):
    return present_value * (i * (i + 1) ** n) / ((1 + i) ** n - 1)


def annual_from_future(future_value, i, n):
    return future_value / ((1 + i) ** n - 1) * i


def nominal_interest(j, m):
    return (1 + j) ** m - 1


def efective_interest(j, m):
    return math.e ** (j * m) - 1
