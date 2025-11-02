from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('student/<int:student_id>/', views.student_profile, name='student'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<slug:course_slug>/', views.CourseView.as_view(), name='course'),
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),
    path('feedback/', views.feedback_view, name='feedback'),
]