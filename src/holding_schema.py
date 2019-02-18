from marshmallow import Schema, fields, validates, ValidationError, EXCLUDE

# {"holding":"Commonwealth Bank of Australia","marketValPercent":8.25647,"marketValue":1.04168334081E9,
# "symbol":"CBA","countryCode":"AU","sectorName":"Diversified Banks","numberofshares":1.4389879E7,
# "currencySymbol":"$"}

class HoldingSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, data_key='holding')
    symbol = fields.Str(required=True, data_key='symbol')
    sector = fields.Str(data_key='sectorName')
    market_val_percent = fields.Decimal(data_key='marketValPercent')
    market_value = fields.Decimal(data_key='marketValue')
    number_of_shares = fields.Decimal(data_key='numberofshares')

    @validates('name')
    def validate_name(self, value):
        self.validate_non_empty_string(value, 'Holding name')

    @validates('symbol')
    def validate_symbol(self, value):
        self.validate_non_empty_string(value, 'Holding symbol')

    def validate_non_empty_string(self, value, field_name):
        if value == '':
            raise ValidationError("{} can't be empty.".format(field_name))
        if value.strip() == '':
            raise ValidationError("{} can't be only white spaces.".format(field_name))
