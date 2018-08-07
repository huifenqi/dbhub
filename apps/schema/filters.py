from django.db.models import Q
from django.forms import TextInput
from django_filters import FilterSet, CharFilter, ModelChoiceFilter

from .models import Database, Table, Column


class ColumnFilter(FilterSet):
    database = ModelChoiceFilter(queryset=Database.objects.all(), method='database_filter', label='',
                                 empty_label='Choose a database')
    table = ModelChoiceFilter(queryset=Table.objects.all(), label='')
    word = CharFilter(method='word_filter', label='',
                      widget=TextInput(attrs={'placeholder': 'Search a word'}))

    def database_filter(self, queryset, name, value):
        return queryset.filter(table__database=value)

    def word_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(comment__icontains=value) | Q(table__name__icontains=value) | Q(
                table__comment__icontains=value))

    class Meta:
        model = Column
        fields = ['database', 'table', 'word']
