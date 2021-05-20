from stocks_core.models import Ticker,Portfolio, Position
from rest_framework import routers, serializers, viewsets


class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticker
        fields = '__all__'
