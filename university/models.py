from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

class UserProfile(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='Логин')
    email = models.EmailField(unique=True, verbose_name='Email')
    password = models.CharField(max_length=128, verbose_name='Пароль')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class Student(models.Model):
    FACULTY_CHOICES = [
        ('FIT', 'Факультет информационных технологий'),
        ('FEFU', 'Дальневосточный федеральный университет'),
        ('FEN', 'Факультет экономики и менеджмента'),
    ]

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    faculty = models.CharField(max_length=10, choices=FACULTY_CHOICES, verbose_name="Факультет")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Course(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность (часы)")
    teacher = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True, verbose_name="Преподаватель")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('completed', 'Завершен'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    enrollment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата записи")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Статус")

    def __str__(self):
        return f"{self.student} - {self.course}"

class Instructor(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    bio = models.TextField(blank=True, verbose_name="Биография")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

