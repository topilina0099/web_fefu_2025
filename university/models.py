from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    FACULTY_CHOICES = [
        ('FIT', 'Факультет информационных технологий'),
        ('FEFU', 'Дальневосточный федеральный университет'),
        ('FEN', 'Факультет экономики и менеджмента'),
    ]

    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    faculty = models.CharField(max_length=10, choices=FACULTY_CHOICES, verbose_name="Факультет")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    description = models.TextField(blank=True, verbose_name="Описание")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student', verbose_name="Роль")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    bio = models.TextField(blank=True, verbose_name="Биография")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    description = models.TextField(blank=True, verbose_name="Описание")

    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='teacher', verbose_name="Роль")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Course(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    duration = models.PositiveIntegerField(verbose_name="Продолжительность (часы)")
    teacher = models.ForeignKey(Instructor, on_delete=models.CASCADE, verbose_name="Преподаватель")
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
    completed_date = models.DateField(null=True, blank=True, verbose_name="Дата завершения")
    grade = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Оценка")

    def __str__(self):
        return f"{self.student} - {self.course}"
