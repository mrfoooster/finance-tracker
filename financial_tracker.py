import calendar
import pandas as pd
import forex_python.converter as forex

from transaction import Transaction


class FinancialTracker:
    def __init__(self, base_currency='USD', filename=""):
        self.base_currency = base_currency
        self.filename = filename
        self.transactions = self.read_csv_file()
        self.converter = forex.CurrencyRates()

    def read_csv_file(self):
        if self.filename != "":
            try:
                data_file = open(self.filename, "r")
                data = data_file.readlines()
                transactions = {}
                for row_index in range(len(data)):
                    if row_index != 0:
                        datas = data[row_index].split(',')
                        transaction = Transaction(datas[0], datas[1], datas[2], datas[3], datas[4])
                        transactions[datas[0]] = transaction
                return transactions
            except FileNotFoundError:
                print('No previous transactions found.')
                return {}
        else:
            return {}

    def write_csv_file(self):
        transaction_data = {
            'Transaction ID': [],
            'Date': [],
            'Type': [],
            'Value': [],
            'Currency': []
        }
        for transaction_id, transaction in self.transactions.items():
            transaction_data['Transaction ID'].append(transaction_id)
            transaction_data['Date'].append(transaction.get_date())
            transaction_data['Type'].append(transaction.get_transaction_type())
            transaction_data['Value'].append(transaction.get_value())
            transaction_data['Currency'].append(transaction.get_currency())

        df = pd.DataFrame(transaction_data)
        df.to_csv('transactions.csv', index=False)

    def add_transaction(self, transaction_id, date, transaction_type, value, currency):
        transaction = Transaction(transaction_id, date, transaction_type, value, currency)
        self.transactions[transaction_id] = transaction

    def convert_currency(self, amount, from_currency, to_currency):
        return self.converter.convert(from_currency, to_currency, amount)

    def get_transactions_values_as(self, target_currency):
        transactions_values = {}
        for transaction_id, transaction in self.transactions.items():
            converted_value = transaction.get_value_as(target_currency)
            transactions_values[transaction.get_date()] = converted_value
        return transactions_values

    def plot_incomes(self, currency):
        incomes = {}
        for transaction_id, transaction in self.transactions.items():
            if transaction.get_transaction_type() == 'Income':
                converted_value = self.convert_currency(transaction.get_value(), transaction.get_currency(), currency)
                incomes[transaction.get_date()] = converted_value
        self.plot_data(incomes, 'Incomes by Date', 'Date', 'Amount')

    def plot_outcomes(self, currency):
        outcomes = {}
        for transaction_id, transaction in self.transactions.items():
            if transaction.get_transaction_type() == 'Outcome':
                converted_value = self.convert_currency(transaction.get_value(), transaction.get_currency(), currency)
                outcomes[transaction.get_date()] = converted_value
        self.plot_data(outcomes, 'Outcomes by Date', 'Date', 'Amount')

    def plot_balance(self, currency):
        balance = {}
        current_balance = 0
        for transaction_id, transaction in self.transactions.items():
            converted_value = self.convert_currency(transaction.get_value(), transaction.get_currency(), currency)
            if transaction.get_transaction_type() == 'Income':
                current_balance += converted_value
            elif transaction.get_transaction_type() == 'Outcome':
                current_balance -= converted_value
            balance[transaction.get_date()] = current_balance
        self.plot_data(balance, 'Balance by Date', 'Date', 'Amount')

    def plot_data(self, data, title, xlabel, ylabel):
        df = pd.DataFrame(list(data.items()), columns=['Date', 'Amount'])
        df.plot(x='Date', y='Amount', kind='bar', title=title, xlabel=xlabel, ylabel=ylabel)

    def show_transactions_on_calendar(self, year, month, view='monthly'):
        cal = calendar.Calendar()

        if view == 'monthly':
            month_calendar = cal.monthdatescalendar(year, month)
            print(calendar.month_name[month], year)
            print("-----------------------------")
            for week in month_calendar:
                for date in week:
                    transactions_on_date = self.get_transactions_on_date(date)
                    if transactions_on_date:
                        print(f"{date.day}:", end=" ")
                        for transaction in transactions_on_date:
                            print(
                                f"{transaction.get_transaction_type()} {transaction.get_value()} {transaction.get_currency()}",
                                end=", ")
                        print()
                print()

        elif view == 'weekly':
            week_calendar = cal.monthdays2calendar(year, month)
            for week in week_calendar:
                print("Week:")
                for day, weekday in week:
                    transactions_on_date = self.get_transactions_on_date(day)
                    if transactions_on_date:
                        print(f"{calendar.day_name[weekday]} {day}:")
                        for transaction in transactions_on_date:
                            print(
                                f"{transaction.get_transaction_type()} {transaction.get_value()} {transaction.get_currency()}")
                        print()

    def get_transactions_on_date(self, date):
        transactions_on_date = []
        for transaction_id, transaction in self.transactions.items():
            if transaction.get_date() == date:
                transactions_on_date.append(transaction)
        return transactions_on_date
