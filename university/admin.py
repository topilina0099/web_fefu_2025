from django.contrib import admin
from .models import Student, Course, Enrollment, UserProfile, Instructor

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'faculty', 'created_at')
    list_filter = ('faculty', 'created_at')
    search_fields = ('last_name', 'first_name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'duration', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'teacher')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'status')
    list_filter = ('status', 'enrollment_date')
    search_fields = ('student__last_name', 'course__title')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    search_fields = ('username', 'email')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email')
    search_fields = ('last_name', 'first_name', 'email')