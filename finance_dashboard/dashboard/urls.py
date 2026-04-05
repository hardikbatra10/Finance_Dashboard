from django.urls import path
from .views import DashboardSummaryView, MonthlyTrendView

urlpatterns = [
    path('summary/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('trends/',  MonthlyTrendView.as_view(),     name='dashboard-trends'),
]