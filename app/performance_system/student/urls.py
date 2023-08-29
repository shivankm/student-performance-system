"""
URL mappings for the staff API.
"""
from django.urls import path

from student import views


app_name = 'student'

urlpatterns = [
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('performance/', views.RetrieveStudentPerformanceView.as_view(), name='performance'),
    path('highest-score/', views.get_highest_total_score, name='highest-score'),
    path('highest-scorers/', views.get_highest_subject_scorers, name='highest-scorers'),
]
