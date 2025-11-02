from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm, LoginForm, FeedbackForm
from .models import UserProfile
from django.urls import reverse

STUDENTS_DATA = {
    1: {
        'info': 'Иван Петров',
        'faculty': 'Кибербезопасность',
        'status': 'Активный',
        'year': 3
    },
    2: {
        'info': 'Мария Сидорова',
        'faculty': 'Информатика',
        'status': 'Активный',
        'year': 2
    },
    3: {
        'info': 'Алексей Козлов',
        'faculty': 'Программная инженерия',
        'status': 'Выпускник',
        'year': 5
    }
}

COURSES_DATA = {
    'python-basics': {
        'name': 'Основы программирования на Python',
        'duration': 36,
        'description': 'Базовый курс по программированию на языке Python для начинающих.',
        'instructor': 'Доцент Петров И.С.',
        'level': 'Начальный'
    },
    'web-security': {
        'name': 'Веб-безопасность',
        'duration': 48,
        'description': 'Курс по защите веб-приложений от современных угроз.',
        'instructor': 'Профессор Сидоров А.В.',
        'level': 'Продвинутый'
    },
    'network-defense': {
        'name': 'Защита сетей',
        'duration': 42,
        'description': 'Изучение методов и технологий защиты компьютерных сетей.',
        'instructor': 'Доцент Козлова М.П.',
        'level': 'Средний'
    }
}

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
            return render(request, 'university/success.html', { 
                'message': 'Вход выполнен успешно! Добро пожаловать в систему.',
                'title': 'Вход в систему'
            })
    else:
        form = LoginForm() 
    
    return render(request, 'university/login.html', { 
        'form': form,  
        'title': 'Вход в систему'
    })

def home_page(request):
   return render(request, 'university/index.html')

class AboutView(View):
   def get(self, request):
        return render(request, 'university/about.html')

def student_profile(request, student_id):
    if student_id in STUDENTS_DATA:
        student_data = STUDENTS_DATA[student_id]
        return render(request, 'university/student_profile.html', {
            'student_id': student_id,
            'student_info': student_data['info'],
            'faculty': student_data['faculty'],
            'status': student_data['status'],
            'year': student_data['year']
        })
    else:
        raise Http404("Студент с таким ID не найден")

class CourseListView(View):
    def get(self, request):
        courses = COURSES_DATA
        context = {'courses': courses}
        return render(request, 'university/courses.html', context)
class CourseView(View):
      def get(self, request, course_slug):
        course = COURSES_DATA.get(course_slug)
        if not course:
            raise Http404('Курс не найден')
        context = {'course_slug': course_slug, 'course': course}
        return render(request, 'university/course.html', context)

def custom_404(request, exception=None):
    return render(request, 'university/not_found.html', status=404)
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            
            return redirect(reverse('success') + '?message=Сообщение отправлено успешно&title=Обратная связь')
    else:
        form = FeedbackForm()

    return render(request, 'university/feedback.html', {
        'form': form,
        'title': 'Обратная связь'
    })