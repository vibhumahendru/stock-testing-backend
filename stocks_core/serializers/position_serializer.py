from stocks_core.models import Ticker,Portfolio, Position
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
import requests
import json

class PositionSerializer(serializers.ModelSerializer):
    ticker_name = serializers.ReadOnlyField(source='ticker.name', read_only=True)
    ticker_cur_code = serializers.ReadOnlyField(source='ticker.currency_code', read_only=True)
    ticker_cur_symbol = serializers.ReadOnlyField(source='ticker.currency_symbol', read_only=True)
    current_price = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ('id','ticker_cur_code','ticker_cur_symbol','current_price', 'created_at', 'num_units','updated_at','buy_date', 'sell_date', 'buy_price', 'sell_price', 'ticker','portfolio', 'ticker_name')

    def get_current_price(self, obj):
        current_price = cache.get(obj.ticker.symbol)
        if current_price:
            return current_price
        else:
            print("NOT FOUND")

    def create(self, validated_data):
        sym = validated_data['ticker'].symbol
        if not cache.get(sym):
            print("NOT FOUN TICICICICIICI")
            r = requests.get(f'http://api.marketstack.com/v1/eod/latest?access_key={settings.MARKETSTACK_API_KEY}&symbols={sym}')
            data = json.loads(r.content)
            cache.set(sym,data['data'][0]['adj_close'])

        obj = Position.objects.create(**validated_data)
        obj.save()
        return obj
