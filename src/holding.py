
class Holding(object):

    def __init__(self, name, symbol, sector, market_val_percent, market_value, number_of_shares):
        self.name = name
        self.symbol = symbol
        self.sector = sector
        self.market_val_percent = market_val_percent
        self.market_value = market_value
        self.number_of_shares = number_of_shares

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.name == other.name and self.symbol == other.symbol and self.sector == other.sector and
            self.market_val_percent == other.market_val_percent and
            self.market_value == other.market_value and
            self.number_of_shares == other.number_of_shares
        )
