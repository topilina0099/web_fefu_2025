from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from django import forms
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import RegistrationForm, LoginForm, FeedbackForm, StudentForm, CourseForm, EnrollmentForm
from .models import UserProfile, Student, Course, Enrollment, Instructor
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages

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
            user = UserProfile(username=username, email=email)
            user.set_password(password)
            user.save()
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
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'university/success.html', {
                    'message': 'Вход выполнен успешно! Добро пожаловать в систему.',
                    'title': 'Вход в систему'
                })
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = LoginForm()
    return render(request, 'university/login.html', {
        'form': form,
        'title': 'Вход в систему'
    })


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

def student_profile(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
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


def custom_404(request, exception=None):
    return render(request, 'university/not_found.html', status=404)

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()  # Сохраняем отзыв в базу
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
    paginate_by = 10  # Добавляем пагинацию

    def get_queryset(self):
        return Student.objects.all().order_by('last_name')

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
    
from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect, get_object_or_404
from .forms import EnrollmentForm

def enrollment_view(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
            print("Form saved")
            return redirect(reverse('success') + '?message=Вы успешно записаны на курс!&title=Запись на курс')
        else:
            print("Form is not valid:", form.errors)  # Вывод ошибок валидации
    else:
        form = EnrollmentForm()

    return render(request, 'university/enrollment.html', {'form': form})


class InstructorListView(ListView):
    model = Instructor
    template_name = 'university/instructors.html'
    context_object_name = 'instructors'

class EnrollmentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label='Имя')
    last_name = forms.CharField(max_length=100, label='Фамилия')
    course = forms.ModelChoiceField(queryset=Course.objects.filter(is_active=True), label='Курс')

    class Meta:
        model = Enrollment
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False

    def save(self, commit=True):
        enrollment = super().save(commit=False)
        student, created = Student.objects.get_or_create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            defaults={'email': f"{self.cleaned_data['first_name'].lower()}.{self.cleaned_data['last_name'].lower()}@example.com"}
        )
        enrollment.student = student
        enrollment.course = self.cleaned_data['course']
        if not self.cleaned_data.get('status'):
            enrollment.status = 'active'  # Значение по умолчанию
        if commit:
            enrollment.save()
        return enrollment
    