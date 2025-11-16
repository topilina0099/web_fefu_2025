from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.urls import path
from . import views
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static

handler404 = views.custom_404

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('course/<int:course_id>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('register/', views.registration_view, name='registration'),  
    path('login/', views.login_view, name='login'), 
    path('success/', views.success_view, name='success'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('enroll/', views.enrollment_view, name='enroll'),
    path('instructors/', views.InstructorListView.as_view(), name='instructor_list'),
    path('logout/', views.logout_view, name='logout'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/profile/edit/', views.edit_student_profile, name='edit_student_profile'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/course/<int:course_id>/', views.manage_course, name='manage_course'),
    path('set_grade/<int:enrollment_id>/', views.set_grade, name='set_grade'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    re_path(r'^accounts/login/$', RedirectView.as_view(url='/login/')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
