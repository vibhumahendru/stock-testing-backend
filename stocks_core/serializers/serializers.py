from stocks_core.models import Ticker,Portfolio, Position
from rest_framework import routers, serializers, viewsets


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    ticker_name = serializers.ReadOnlyField(source='ticker.name', read_only=True)

    class Meta:
        model = Position
        fields = ('id', 'created_at', 'num_units','updated_at','buy_date', 'sell_date', 'buy_price', 'sell_price', 'ticker','portfolio', 'ticker_name')
