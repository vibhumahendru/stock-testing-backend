from django.db import models
from .timestamp_fields import TimeStampMixin
from django.contrib.auth.models import User


class MyException(Exception):
    pass

class Ticker(TimeStampMixin):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=200)
    currency_code = models.CharField(max_length=200)
    currency_symbol = models.CharField(max_length=200)
    exchange = models.CharField(max_length=200)


    def __str__(self):
        return self.name


class Portfolio(TimeStampMixin):
    name = models.CharField(max_length=200)
    note = models.CharField(max_length=600, null=True, blank=True,)
    pnl = models.FloatField(null=True, blank=True, default=0)
    balance = models.IntegerField(null=False, blank=False, default=10000)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Position(TimeStampMixin):
    ticker = models.ForeignKey(Ticker, null=False, blank=False,on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, null=False, blank=False, on_delete=models.CASCADE, related_name="positions")
    buy_date = models.DateTimeField(null=False, blank=False)
    sell_date = models.DateTimeField(null=True, blank=True)
    buy_price = models.DecimalField(null=False, blank=False, max_digits=100, decimal_places=3)
    sell_price = models.DecimalField(null=True, blank=True,max_digits=100, decimal_places=3)
    num_units = models.IntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return self.ticker.name

    def save(self, *args, **kwargs):
        all_positions = self.portfolio.positions.all()
        unique_positions = all_positions.values("ticker__currency_code").distinct()

        if len(unique_positions):
            if unique_positions[0]['ticker__currency_code'] != self.ticker.currency_code:
                raise MyException("this is a message")


        super(Position, self).save(*args, **kwargs)














        #
