from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Student, Course, Enrollment

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=[
            ('student', 'Студент'),
            ('teacher', 'Преподаватель'),
        ],
        label='Роль',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username.strip()) < 3:
            raise ValidationError("Логин должен содержать минимум 3 символа")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Это имя пользователя уже занято")
        return username.strip()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@students.dvfu.ru'):
            raise ValidationError("Используйте корпоративную почту @students.dvfu.ru")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    

class FeedbackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Ваше имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Ваш email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Ваше сообщение',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
   
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'birth_date', 'faculty', 'avatar', 'phone', 'description']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration', 'teacher', 'is_active']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course', 'status']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        if student:
            self.fields['course'].queryset = Course.objects.filter(is_active=True).exclude(enrollment__student=student)

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'birth_date', 'faculty', 'avatar', 'phone', 'description']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
class GradeForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['grade', 'status', 'completed_date']
        widgets = {
            'completed_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }