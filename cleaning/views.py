from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, RequestForm
from .models import Request

# Function to check if the user is not an admin
def is_not_admin(user):
    return user.username != 'adminka'

# Главная страница
def home(request):
    return render(request, 'cleaning/home.html')

# Представление регистрации
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_request')
            else:
                return render(request, 'cleaning/register.html', {'form': form, 'error': 'Ошибка аутентификации'})
    else:
        form = CustomUserCreationForm()

    return render(request, 'cleaning/register.html', {'form': form})

# Страница входа
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.username == 'adminka':
                return redirect('admin_panel')
            return redirect('create_request')
        else:
            return render(request, 'cleaning/login.html', {'form': form, 'error': 'Неверный логин или пароль'})
    else:
        form = AuthenticationForm()

    return render(request, 'cleaning/login.html', {'form': form})


# Страница выхода
def logout_view(request):
    logout(request)
    return render(request, 'cleaning/logout.html')

@login_required
@user_passes_test(is_not_admin, login_url='home')
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.save()
            return redirect('request_list')
    else:
        form = RequestForm()

    return render(request, 'cleaning/create_request.html', {'form': form})

# Страница списка заявок пользователя
@login_required
@user_passes_test(is_not_admin, login_url='home')
def request_list(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'cleaning/request_list.html', {'requests': user_requests})

# Проверка, является ли пользователь админом
def is_admin(user):
    return user.username == 'adminka'

# Панель администратора (доступ только для админа)
@user_passes_test(is_admin, login_url='home')
def admin_panel(request):
    requests = Request.objects.all()
    return render(request, 'cleaning/admin_panel.html', {'requests': requests})

# Изменение статуса заявки администратором
@user_passes_test(is_admin, login_url='home')
def change_status(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        cancel_reason = request.POST.get('cancel_reason')
        if status:
            req.status = status
        if cancel_reason:
            req.cancel_reason = cancel_reason
        req.save()
        return redirect('admin_panel')

    return redirect('admin_panel')
