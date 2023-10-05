from django_filters import rest_framework as filters

from schedule.models import Homework


class HomeworkFilterSet(filters.FilterSet):
    deadline_range = filters.DateFromToRangeFilter(field_name='deadline')

    class Meta:
        model = Homework
        fields = ('deadline_range',)