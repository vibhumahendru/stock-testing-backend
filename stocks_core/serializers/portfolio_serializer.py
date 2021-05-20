from stocks_core.models import Ticker,Portfolio, Position
from stocks_core.serializers.position_serializer import PositionSerializer
from rest_framework import routers, serializers, viewsets
import requests
import json


class PortfolioSerializer(serializers.ModelSerializer):
    equity_investment = serializers.SerializerMethodField()
    actualised_return = serializers.SerializerMethodField()
    equity_valuation = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = '__all__'

    def get_equity_investment(self, obj):
        positions = obj.positions.filter(sell_date__isnull=True)
        investment = 0
        for p in positions:
            investment += p.buy_price * p.num_units
        return investment

    def get_actualised_return(self, obj):
        positions = obj.positions.filter(sell_date__isnull=False)
        actualised = 0
        for p in positions:
            actualised += ((p.sell_price - p.buy_price) * p.num_units)

        return actualised

    def get_equity_valuation(self, obj):
        """
        get only unique buy positions
        fetch current price of each position
        inside for loop : valuation += quantity * current price

        """
        open_positions = obj.positions.filter(sell_price__isnull=True)
        #schema = [{'ticker__symbol': 'AAPL'}, {'ticker__symbol': 'MSFT'}]
        open_postion_symbols = open_positions.values("ticker__symbol").distinct()
        price_dict = self.fetch_current_price(open_postion_symbols)

        valuation = 0
        for p in open_positions:
            valuation += (p.num_units * price_dict[p.ticker.symbol])
        return valuation

    def fetch_current_price(self, symbols):
        price_dict = {}
        for s in symbols:
            sym = s['ticker__symbol']
            r = requests.get(f'http://api.marketstack.com/v1/eod/latest?access_key=ce8415abdd92171bffe3063e2361ecd4&symbols={sym}')
            data = json.loads(r.content)
            price_dict[s['ticker__symbol']] = data['data'][0]['adj_close']
        return price_dict





















        # e
