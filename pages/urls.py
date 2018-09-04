from django.urls import path
from . import views

urlpatterns = [
    path('', views.PagesListView.as_view(), name='pages'),
    path('<int:pk>/<slug:slug>/', views.PagesDetailView.as_view(), name='page'),
    path('create/', views.PageCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.PageUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', views.PageDeleteView.as_view(), name='delete')
]