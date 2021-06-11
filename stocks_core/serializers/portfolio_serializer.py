from stocks_core.models import Ticker,Portfolio, Position
from stocks_core.serializers.position_serializer import PositionSerializer
from rest_framework import routers, serializers, viewsets
import requests
import json
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
import pandas as pd
import os
from decimal import Decimal


nifty_csv_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../nifty_data.csv')
nifty_df = pd.read_csv(nifty_csv_path)


class PortfolioSerializer(serializers.ModelSerializer):
    equity_investment = serializers.SerializerMethodField()
    actualised_return = serializers.SerializerMethodField()
    equity_valuation = serializers.SerializerMethodField()
    portfolio_currency = serializers.SerializerMethodField()
    num_positions = serializers.SerializerMethodField()
    num_unique_stocks = serializers.SerializerMethodField()
    nifty_comparison = serializers.SerializerMethodField()

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
        positions = obj.positions.filter(sell_date__isnull=False, sell_price__isnull=False)
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
        open_positions = obj.positions.filter(sell_price__isnull=True, sell_date__isnull=True)
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
            latest_cached = cache.get(sym)
            if latest_cached:
                price_dict[sym] = latest_cached
            else:
                r = requests.get(f'http://api.marketstack.com/v1/eod/latest?access_key={settings.MARKETSTACK_API_KEY}&symbols={sym}')
                data = json.loads(r.content)
                price_dict[s['ticker__symbol']] = data['data'][0]['adj_close']
                cache.set(sym,data['data'][0]['adj_close'])

        return price_dict

    def get_portfolio_currency(self,obj):
        if obj.positions.first():
            return obj.positions.first().ticker.currency_symbol
        else:
            return None

    def get_num_positions(self, obj):
        return len(obj.positions.all())

    def get_num_unique_stocks(self, obj):
        return len(obj.positions.all().values("ticker__symbol").distinct())


    def get_nifty_comparison(self, obj):
        try:
            unique_date = obj.positions.all().values("buy_date").distinct()

            total_dates = {}
            # total_dates = {
            #     date1:total_invested
            # }

            time_format = '%d-%b-%Y'

            for p in obj.positions.all():
                if p.buy_date.strftime(time_format) in total_dates:
                    total_dates[p.buy_date.strftime(time_format)] += p.buy_price * p.num_units
                else:
                    total_dates[p.buy_date.strftime(time_format)] = p.buy_price * p.num_units

            total_nifty_units = 0
            total_invested_in_nifty = 0

            for date in total_dates:
                """
                get nifty price on that day
                calc num units bought of nifty on that day
                sum nifty units, sum invested total
                nifty units * latest price
                compare with invested total
                """

                try:
                    row = nifty_df[nifty_df['Date'] == date]
                    close_price = Decimal(row['Close'].iloc[0])
                    total_invested_on_day = total_dates[date]
                    # print(type(total_invested_on_day), "total_invested_on_day")
                    # print(type(close_price), "close_price")
                    nifty_units = total_invested_on_day / close_price

                    print(nifty_units, "nifty_units")
                    print(total_invested_on_day, "total_invested_on_day")

                    total_nifty_units += nifty_units
                    total_invested_in_nifty += total_invested_on_day


                except Exception as e:
                    pass
            #
            # print(total_nifty_units, "total_nifty_units")
            # print(total_invested_in_nifty, "total_invested_in_nifty")

            total_nifty_value = Decimal(nifty_df.iloc[[-1]]['Close'].iloc[0]) * total_nifty_units
            print(total_nifty_value, "total_nifty_value")
            percent_change = ((total_nifty_value - total_invested_in_nifty) / total_invested_in_nifty) * 100

            return round(percent_change, 2)
        except Exception as e:
            return 0
        # print(nifty_df)























        # e
