from django.shortcuts import render
from .serializers import TickerSerializer
from stocks_core.models import *
from stocks_core.serializers import *
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes



class TickerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TickerSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Ticker.objects.all()


class PortfolioViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PortfolioSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user']=request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





class PositionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PositionSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['portfolio']

    def get_queryset(self):

        return Position.objects.filter(portfolio__user=self.request.user)
