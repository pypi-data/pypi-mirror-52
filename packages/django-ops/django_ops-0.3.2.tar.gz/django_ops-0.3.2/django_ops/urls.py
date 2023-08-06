from django.urls import path

from . import views

urlpatterns = [
    path('', views.RootView.as_view(), name="root"),
    path('ping/',  views.PingView.as_view(), name="ping"),
    path('info/', views.InfoView.as_view(), name="info"),
    path('migration/', views.MigrationView.as_view(), name="migration"),
]
