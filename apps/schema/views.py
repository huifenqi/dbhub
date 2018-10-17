from django_filters.views import FilterView
from django_tables2 import SingleTableMixin
from django.conf import settings

from .tables import ColumnTable
from .models import Column
from .filters import ColumnFilter


class ColumnListView(SingleTableMixin, FilterView):
    table_class = ColumnTable
    model = Column
    template_name = "columns.html"
    filterset_class = ColumnFilter

    def get_queryset(self):
        return super(ColumnListView, self).get_queryset().select_related("table")

    def get_context_data(self, **kwargs):
        ctx = super(ColumnListView, self).get_context_data(**kwargs)
        ctx['title'] = settings.TITLE
        ctx['enable_oauth'] = settings.ENABLE_OAUTH
        return ctx
