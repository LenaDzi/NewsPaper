from django_filters import FilterSet, DateTimeFilter
from .models import *
from django.forms import DateInput


class PostFilter(FilterSet):
    dataCreation = DateTimeFilter(
        field_name='dataCreation',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        ),
    )

    class Meta:
        model = Post
        fields = {
            'categoryType': ['exact'],
            'title': ['icontains'],
        }