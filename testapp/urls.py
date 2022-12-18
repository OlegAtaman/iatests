from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path("", TemplateView.as_view(template_name="home.html"), name="main"),
    # path("profile/", views.profile_view, name="profile"),
    # path("profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    # path("addsubject/", views.SubjectAddingView.as_view(), name="add_subject"),
    # path("c/<code>/", views.CourseView.as_view(), name="course"),
    # path("new_course/", views.NewCourseView.as_view(), name="add_course"),
    # path("join_course/", views.JoinCourseView.as_view(), name="join_course"),
    # path("c/<code>/new_test/", views.NewTestView.as_view(), name="add_test"),
    # path("c/<code>/t/<id>/", views.TestView.as_view(), name="test"),
    # path("c/<code>/t/<id>/overview/", views.testoverview, name="t_overview"),
    # path("c/<code>/overview/", views.course_overview, name="c_overview"),
    # path("c/<code>/delete/", views.delete_course, name="delete_course"),
    path("course/<int:pk>/", views.CourseDetailView.as_view(), name="course"),
    path("teacher/<int:pk>/", views.TeacherProfileDetailView.as_view(), name="teacher-profile"),
    path("teacher/<int:pk>/edit", views.TeacherProfileUpdateView.as_view(), name="teacher-edit"),
    path("student/<int:pk>/", views.StudentProfileDetailView.as_view(), name="student-profile"),
    path("student/<int:pk>/edit", views.StudentProfileUpdateView.as_view(), name="student-edit"),

    path("submission/<int:pk>/", views.SubmissionDetailView.as_view(), name="submission"),
]
