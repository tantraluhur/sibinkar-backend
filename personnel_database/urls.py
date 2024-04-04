from django.urls import path
from personnel_database.views.pangkat_views import PangkatView
from personnel_database.views.personil_views import PersonilView
from personnel_database.views.posisi_views import PosisiView

urlpatterns = [
    path('pangkat/', PangkatView.as_view()),
    path('posisi/', PosisiView.as_view()),
    path('personil/', PersonilView.as_view()),

]