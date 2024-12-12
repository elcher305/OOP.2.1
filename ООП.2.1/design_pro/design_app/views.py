from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, RequestForm, CategoryForm
from .models import Request, Category

# Главная страница
def home(request):
    completed_requests = Request.objects.filter(status='completed').order_by('-created_at')[:4]
    in_progress_count = Request.objects.filter(status='in_progress').count()
    return render(request, 'home.html', {'completed_requests': completed_requests, 'in_progress_count': in_progress_count})

# Страница входа
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})
    return render(request, 'login.html')

# Страница регистрации
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# Личный кабинет пользователя
@login_required
def dashboard(request):
    user_requests = Request.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'user_requests': user_requests})

# Создание заявки
@login_required
def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.user = request.user
            request_obj.save()
            return redirect('dashboard')
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form})

# Удаление заявки
@login_required
def delete_request(request, request_id):
    req = Request.objects.get(id=request_id)
    if req.user == request.user and req.status not in ['in_progress', 'completed']:
        req.delete()
    return redirect('dashboard')

# Просмотр заявок администратором
@login_required
def admin_dashboard(request):
    if request.user.is_staff:
        requests = Request.objects.all().order_by('-created_at')
        return render(request, 'admin_dashboard.html', {'requests': requests})
    else:
        return redirect('home')

# Смена статуса заявки
@login_required
def change_status(request, request_id):
    if request.user.is_staff:
        req = Request.objects.get(id=request_id)
        if req.status == 'new':
            if 'in_progress' in request.POST:
                req.status = 'in_progress'
                req.save()
            elif 'completed' in request.POST:
                req.status = 'completed'
                req.save()
        return redirect('admin_dashboard')
    else:
        return redirect('home')

# Управление категориями
@login_required
def manage_categories(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('manage_categories')
        else:
            form = CategoryForm()
        categories = Category.objects.all()
        return render(request, 'manage_categories.html', {'form': form, 'categories': categories})
    else:
        return redirect('home')

# Удаление категории
@login_required
def delete_category(request, category_id):
    if request.user.is_staff:
        cat = Category.objects.get(id=category_id)
        cat.delete()
        return redirect('manage_categories')
    else:
        return redirect('home')

# Выход
def logout_view(request):
    logout(request)
    return redirect('home')