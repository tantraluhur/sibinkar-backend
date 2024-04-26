from django.urls import path
from staffing_status.views import StaffingStatusView

urlpatterns = [
    path('', StaffingStatusView.as_view()),
]