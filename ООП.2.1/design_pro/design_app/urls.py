from django.urls import path
from . import views

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Вход и регистрация
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Личный кабинет пользователя
    path('dashboard/', views.dashboard, name='dashboard'),

    # Создание и удаление заявки
    path('create_request/', views.create_request, name='create_request'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),

    # Панель администратора
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('change_status/<int:request_id>/', views.change_status, name='change_status'),

    # Управление категориями
    path('manage_categories/', views.manage_categories, name='manage_categories'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
]