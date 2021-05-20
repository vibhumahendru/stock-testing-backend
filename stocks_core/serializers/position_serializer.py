from stocks_core.models import Ticker,Portfolio, Position
from rest_framework import routers, serializers, viewsets

class PositionSerializer(serializers.ModelSerializer):
    ticker_name = serializers.ReadOnlyField(source='ticker.name', read_only=True)

    class Meta:
        model = Position
        fields = ('id', 'created_at', 'num_units','updated_at','buy_date', 'sell_date', 'buy_price', 'sell_price', 'ticker','portfolio', 'ticker_name')
