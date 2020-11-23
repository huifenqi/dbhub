from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django.conf import settings
from dal import autocomplete

from .tables import ColumnTable
from .models import Column, Table
from .filters import ColumnFilter


class ColumnListView(SingleTableMixin, FilterView):
    table_class = ColumnTable
    model = Column
    template_name = "columns.html"
    filterset_class = ColumnFilter
    paginate_by = settings.DEFAULT_PAGE_SIZE

    def get_queryset(self):
        return super(ColumnListView, self).get_queryset().select_related("table")

    def get_context_data(self, **kwargs):
        ctx = super(ColumnListView, self).get_context_data(**kwargs)
        ctx['title'] = settings.TITLE
        ctx['enable_oauth'] = settings.ENABLE_OAUTH
        return ctx


class TableAutocomplete(autocomplete.Select2QuerySetView):
    def dispatch(self, request, *args, **kwargs):
        self.database = request.GET.get('database', None)
        return super(TableAutocomplete, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = Table.objects.all()
        if self.database:
            qs = qs.filter(database=self.database)
        if self.q:
            qs = qs.filter(name__contains=self.q)
        return qs
