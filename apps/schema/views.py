from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .tables import ColumnTable
from .models import Column
from .filters import ColumnFilter


class ColumnListView(SingleTableMixin, FilterView):
    table_class = ColumnTable
    model = Column
    template_name = "semantic_template.html"
    filterset_class = ColumnFilter

    def get_queryset(self):
        return super(ColumnListView, self).get_queryset().select_related("table")
