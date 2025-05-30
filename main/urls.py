from django.urls import path
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('menu/', views.menu_view, name='menu'),
    
    # Бронирование
    path('reservation/', views.reservation, name='reservation'),
    path('reservation/success/', views.reservation_success, name='reservation_success'),
    
    # Регистрация
    path('register/', views.register, name='register'),
    path('news/', views.news_list, name='news'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail'),
]
