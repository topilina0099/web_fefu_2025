from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Instructor

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student'

class InstructorInline(admin.StackedInline):
    model = Instructor
    can_delete = False
    verbose_name_plural = 'Instructor'

class CustomUserAdmin(UserAdmin):
    inlines = (StudentInline, InstructorInline)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'faculty')
    search_fields = ('first_name', 'last_name', 'email', 'faculty')
    list_filter = ('faculty',)

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'is_active')
    search_fields = ('title', 'teacher__first_name', 'teacher__last_name')
    list_filter = ('is_active',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'grade', 'enrollment_date')
    search_fields = ('student__first_name', 'student__last_name', 'course__title')
    list_filter = ('status', 'course')
