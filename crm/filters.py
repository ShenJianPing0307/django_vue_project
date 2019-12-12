from django_filters.rest_framework import filterset
import django_filters
from django.db.models import Q
from crm.models import *

from django_filters import rest_framework as filters

class UserInfoFilter(filters.filterset):

    class Meta:
        model = UserInfo
        fields = ['username', ]


