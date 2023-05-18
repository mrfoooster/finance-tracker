import forex_python.converter as forex


class Transaction:
    def __init__(self, transaction_id, date, transaction_type, value, currency):
        self.transaction_id = transaction_id
        self.date = date
        self.transaction_type = transaction_type
        self.value = value
        self.currency = currency

    def set_date(self, date):
        self.date = date

    def set_transaction_type(self, transaction_type):
        self.transaction_type = transaction_type

    def set_value(self, value):
        self.value = value

    def set_currency(self, currency):
        self.currency = currency

    def get_date(self):
        return self.date

    def get_transaction_type(self):
        return self.transaction_type

    def get_value(self):
        return self.value

    def get_currency(self):
        return self.currency

    def get_value_as(self, target_currency):
        converter = forex.CurrencyRates()
        converted_value = converter.convert(self.value, self.currency, target_currency)
        return converted_value
