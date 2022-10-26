from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='main'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
]