from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from django.views import View
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib import messages
from .forms import StudentProfileForm
from .forms import RegistrationForm, LoginForm, FeedbackForm, GradeForm, CourseForm, EnrollmentForm
from .models import Student, Course, Enrollment, Instructor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

def success_view(request):
    return render(request, 'university/success.html', {
        'message': request.GET.get('message', 'Операция выполнена успешно!'),
        'title': request.GET.get('title', 'Успех')
    })

def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            role = form.cleaned_data['role']

            # Создаём пользователя
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Создаём связанный профиль (Student или Instructor)
            if role == 'student':
                Student.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    role=role
                )
            elif role == 'teacher':
                Instructor.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    role=role
                )
            login(request, user)
            return render(request, 'university/success.html', {
                'message': 'Регистрация прошла успешно!',
                'title': 'Регистрация'
            })
    else:
        form = RegistrationForm()
    return render(request, 'university/registration.html', {
        'form': form,
        'title': 'Регистрация'
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'university/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home_page(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.filter(is_active=True).count()
    recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
    return render(request, 'university/home.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'recent_courses': recent_courses,
    })

class AboutView(View):
    def get(self, request):
        return render(request, 'university/about.html')

@login_required
def student_profile(request, student_id):
    try:
        student = Student.objects.get(id=student_id, user=request.user)
        return render(request, 'university/student_profile.html', {
            'student': student,
        })
    except Student.DoesNotExist:
        raise Http404("Студент с таким ID не найден")

class CourseListView(ListView):
    model = Course
    template_name = 'university/courses.html'
    context_object_name = 'courses'
    def get_queryset(self):
        return Course.objects.all()

class CourseDetailView(DetailView):
    model = Course
    template_name = 'university/course.html'
    context_object_name = 'course'
    pk_url_kwarg = 'course_id'
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_active:
            raise Http404("Курс неактивен или не найден.")
        return obj

def custom_404(request, exception=None):
    return render(request, 'university/not_found.html', status=404)

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            return redirect(reverse('success') + '?message=Сообщение отправлено успешно&title=Обратная связь')
    else:
        form = FeedbackForm()
    return render(request, 'university/feedback.html', {
        'form': form,
        'title': 'Обратная связь'
    })

class StudentListView(ListView):
    model = Student
    template_name = 'university/students.html'
    context_object_name = 'students'
    paginate_by = 10
    def get_queryset(self):
        return Student.objects.all().order_by('last_name')

@login_required
def enrollment_view(request):
    course_id = request.GET.get('course')
    course = get_object_or_404(Course, id=course_id)
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        if created:
            messages.success(request, 'Вы успешно записаны на курс!')
        else:
            messages.warning(request, 'Вы уже записаны на этот курс!')
        return redirect(reverse('success'))

    return render(request, 'university/enrollment.html', {'course': course})
class InstructorListView(ListView):
    model = Instructor
    template_name = 'university/instructors.html'
    context_object_name = 'instructors'

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrap(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if hasattr(user, 'student') and user.student.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                if hasattr(user, 'instructor') and user.instructor.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrap
    return decorator

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, 'university/admin_dashboard.html')

@role_required(allowed_roles=['teacher'])
def teacher_dashboard(request):
    return render(request, 'university/teacher_dashboard.html')

@role_required(allowed_roles=['teacher', 'admin'])
def manage_courses(request):
    return render(request, 'university/manage_courses.html')

@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    enrollments = Enrollment.objects.filter(student=student)
    completed_courses = enrollments.filter(status='completed').order_by('-completed_date')

    return render(request, 'university/student_dashboard.html', {
        'student': student,
        'enrollments': enrollments,
        'completed_courses': completed_courses,
    })
@login_required
def edit_student_profile(request):
    # Попробуем получить объект Student для текущего пользователя
    student, created = Student.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')
    else:
        form = StudentProfileForm(instance=student)

    return render(request, 'university/edit_student_profile.html', {'form': form})
@login_required
def teacher_dashboard(request):
    instructor = get_object_or_404(Instructor, user=request.user)
    courses = Course.objects.filter(teacher=instructor)
    return render(request, 'university/teacher_dashboard.html', {
        'instructor': instructor,
        'courses': courses,
    })

@login_required
def manage_course(request, course_id):
    instructor = get_object_or_404(Instructor, user=request.user)
    course = get_object_or_404(Course, id=course_id, teacher=instructor)
    enrollments = Enrollment.objects.filter(course=course)

    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        enrollment = get_object_or_404(Enrollment, id=enrollment_id, course=course)
        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, "Оценка успешно выставлена!")
            return redirect('manage_course', course_id=course.id)
    else:
        form = GradeForm()

    return render(request, 'university/manage_course.html', {
        'course': course,
        'enrollments': enrollments,
        'form': form,

    })

@login_required
def set_grade(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    instructor = get_object_or_404(Instructor, user=request.user)

    # Проверка, что преподаватель ведет курс, на который записан студент
    if enrollment.course.teacher != instructor:
        messages.error(request, "У вас нет прав для выставления оценок на этом курсе.")
        return redirect('manage_course', course_id=enrollment.course.id)

    if request.method == 'POST':
        grade = request.POST.get('grade')
        status = request.POST.get('status')
        completed_date = request.POST.get('completed_date')

        enrollment.grade = int(grade) if grade else None
        enrollment.status = status
        enrollment.completed_date = completed_date if completed_date else None
        enrollment.save()

        messages.success(request, "Оценка успешно выставлена!")
        return redirect('manage_course', course_id=enrollment.course.id)
    
def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_instructors = Instructor.objects.count()
    total_courses = Course.objects.count()

    context = {
        'total_students': total_students,
        'total_instructors': total_instructors,
        'total_courses': total_courses,
    }
    return render(request, 'university/admin_dashboard.html', context)