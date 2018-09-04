from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='profiles'),
    path('profile/<username>/', views.ProfileDetailView.as_view(), name='detail_profile')
]