"""track_stocks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import url, include
from stocks_core.views import *


ticker_router = routers.DefaultRouter()
ticker_router.register(r'', TickerViewSet, basename='ticker')

portfolio_router = routers.DefaultRouter()
portfolio_router.register(r'', PortfolioViewSet, basename='portfolio')

position_router = routers.DefaultRouter()
position_router.register(r'', PositionViewSet, basename='position')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^ticker/', include(ticker_router.urls)),
    url(r'^portfolio/', include(portfolio_router.urls)),
    url(r'^position/', include(position_router.urls)),
]
