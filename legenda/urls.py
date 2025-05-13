"""legenda URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from main.views import register, menu_view, reservation, reservation_success, delete_reservation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('menu/', menu_view, name='menu'),  # Используем представление menu_view
    path('reservation/', reservation, name='reservation'),  # Используем представление reservation
    path('reservation/delete/<int:reservation_id>/', delete_reservation, name='delete_reservation'),
    path('reservation/success/', reservation_success, name='reservation_success'),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),
    path('register/', register, name='register'),  # Добавляем маршрут для регистрации
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
