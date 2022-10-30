from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='main'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('addsubject/', views.SubjectAddingView.as_view(), name='add_subject'),
    path('c/<code>/', views.CourseView.as_view(), name='course'),
    path('new_course/', views.NewCourseView.as_view(), name='add_course'),
    path('join_course/', views.JoinCourseView.as_view(), name='join_course'),
]