from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'), 
    path('about/', views.AboutView.as_view(), name='about'),
    path('student/<int:student_id>/', views.student_profile, name='student'),
    path('courses/', views.CourseListView.as_view(), name='courses'),
    path('course/<slug:course_slug>/', views.CourseView.as_view(), name='course'),
]