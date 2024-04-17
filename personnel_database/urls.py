from django.urls import path
from personnel_database.views.pangkat_views import PangkatView
from personnel_database.views.user_personil_views import PersonilView
from personnel_database.views.subdit_views import SubditView
from personnel_database.views.subsatker_views import SubSatKerView
from personnel_database.views.jabatan_views import JatabanView

urlpatterns = [
    path('pangkat/', PangkatView.as_view()),
    path('subdit/', SubditView.as_view()),
    path('subsatker/', SubSatKerView.as_view()),
    path('jabatan/', JatabanView.as_view()),
    path('', PersonilView.as_view()),
    path('<str:personil_id>/', PersonilView.as_view()),
]