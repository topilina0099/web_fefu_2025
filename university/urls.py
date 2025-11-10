from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('register/', views.registration_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('enroll/', views.enrollment_view, name='enroll'),
    path('instructors/', views.InstructorListView.as_view(), name='instructor_list'),  # Новый маршрут
]
