from django.db import models
from .timestamp_fields import TimeStampMixin

class Ticker(TimeStampMixin):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Portfolio(TimeStampMixin):
    name = models.CharField(max_length=200)
    note = models.CharField(max_length=600)
    pnl = models.FloatField(null=True, blank=True, default=0)
    balance = models.IntegerField(null=False, blank=False, default=10000)

    def __str__(self):
        return self.name

class Position(TimeStampMixin):
    ticker = models.ForeignKey(Ticker, null=False, blank=False,on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, null=False, blank=False, on_delete=models.CASCADE)
    buy_date = models.DateTimeField(null=False, blank=False)
    sell_date = models.DateTimeField(null=True, blank=True)
    buy_price = models.IntegerField(null=False, blank=False)
    sell_price = models.IntegerField(null=True, blank=True)
    num_units = models.IntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return self.ticker
