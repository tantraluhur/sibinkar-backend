from django.urls import path

from organizational_structure.views.chart_view import ChartView, ChartDetailView
from organizational_structure.views.node_view import ChildNodeView, OffsetChildNodeView

urlpatterns = [
    path('chart/', ChartView.as_view()),
    path('chart/<int:id>/', ChartDetailView.as_view()),
    path('nodes/<int:chart_id>/', ChildNodeView.as_view()),
    path('offset-nodes/<int:chart_id>/', OffsetChildNodeView.as_view())
]