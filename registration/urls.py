from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/email/', views.UpdateEmailView.as_view(), name='update_email')
]