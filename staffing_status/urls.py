from django.urls import path
from staffing_status.views import StaffingStatusView, StaffingStatusPangkatView

urlpatterns = [
    path('', StaffingStatusView.as_view()),
    path('total/', StaffingStatusPangkatView.as_view())
]