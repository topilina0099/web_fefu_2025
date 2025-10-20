from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render
from django.views import View

def home_page(request):
    '''представление, которое рендерит шаблон index.html.'''
    return render(request, 'university/index.html', {})

class AboutView(View):
    '''Class-Based Views для получения страницы О нас'''
    def get(self, request):
        return render(request, 'university/about.html', {})

def student_profile(request, student_id):
    '''представление, которое рендерит страницы шаблонов динамически 
    для студентов с номерами от 1 до 100, иначе возвращает 404
    и кнопки переходов между страницами студентов '''
    if student_id > 100 or student_id < 1:
        return render(request, 'university/not_found.html', status=404)
    context = {
        'student_id': student_id,
        'name': f'Мишутка Шуткин (пример {student_id})',
        'group': 'C9121-10.03.01ммзи',
        'prev_id': student_id - 1 if student_id > 1 else None,
        'next_id': student_id + 1 if student_id < 100 else None,
    }
    return render(request, 'university/student.html', context)


class CourseListView(View):
    '''Страница со списком курсов'''
    def get(self, request):
        courses = CourseView.COURSES
        context = {'courses': courses}
        return render(request, 'university/courses.html', context)


class CourseView(View):
    '''Страницы с курсами для динамической отрисовки'''
    COURSES = {
        'introduction-to-django': 'Введение в Django',
        'web-technologies': 'Веб-технологии',
        'python-basics': 'Основы Python'
    }

    def get(self, request, course_slug):
        title = self.COURSES.get(course_slug)
        if not title:
            raise Http404('Курс не найден')
        context = {'course_slug': course_slug, 'title': title}
        return render(request, 'university/course.html', context)
    
def custom_404(request, exception=None):
    '''специанльная страница для ошибки 404'''
    return render(request, 'university/not_found.html', status=404)
    