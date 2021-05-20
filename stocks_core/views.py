from django.shortcuts import render
from .serializers import TickerSerializer
from stocks_core.models import *
from stocks_core.serializers import *
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class TickerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = TickerSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Ticker.objects.all()

class PortfolioViewSet(viewsets.ModelViewSet):
    """ 
    A viewset for viewing and editing user instances.
    """
    serializer_class = PortfolioSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Portfolio.objects.all()

class PositionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['portfolio']

    def get_queryset(self):
        return Position.objects.all()
