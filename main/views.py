from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ReservationForm, UserRegisterForm, FeedbackForm
import logging
import json
from django.contrib.auth.forms import UserCreationForm
from .models import MenuItem, MenuPhoto, Reservation, News, GalleryPhoto
from datetime import date

logger = logging.getLogger(__name__)

def home(request):
    try:
        if request.method == 'POST' and 'feedback_form' in request.POST:
            logger.info("Processing feedback form submission")
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = form.save()
                logger.info(f"Feedback saved successfully: {feedback.id}")
                return JsonResponse({'status': 'success'})
            else:
                logger.warning(f"Form validation failed: {form.errors}")
                return JsonResponse({
                    'status': 'error',
                    'errors': {
                        field: [str(error) for error in errors]
                        for field, errors in form.errors.items()
                    }
                })
        
        feedback_form = FeedbackForm()
        return render(request, 'index.html', {
            'feedback_form': feedback_form
        })
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='login')
def reservation(request):
    # Получаем все бронирования текущего пользователя
    user_reservations = Reservation.objects.filter(user=request.user).order_by('-date', '-time')
    today = date.today()
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.user = request.user  # Привязываем к пользователю
                reservation.save()
                logger.info(f"Бронирование сохранено: ID={reservation.id}")
                
                # Отправка уведомления администратору
                subject = 'Новое бронирование'
                message = f'''
                Новое бронирование:
                
                Имя: {reservation.name}
                Email: {reservation.email}
                Телефон: {reservation.phone}
                Дата: {reservation.date}
                Время: {reservation.time}
                Количество гостей: {reservation.guests}
                Сообщение: {reservation.message or 'Нет сообщения'}
                '''
                
                try:
                    logger.info(f"Попытка отправки уведомления о бронировании {reservation.id}")
                    logger.info(f"Отправка на email: {settings.ADMIN_EMAIL}")
                    logger.info(f"Отправка с email: {settings.DEFAULT_FROM_EMAIL}")
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.ADMIN_EMAIL],
                        fail_silently=False,
                    )
                    logger.info(f"Уведомление о бронировании {reservation.id} успешно отправлено на {settings.ADMIN_EMAIL}")
                    messages.success(request, 'Уведомление о бронировании отправлено администратору!')
                except Exception as e:
                    logger.error(f"Ошибка при отправке уведомления о бронировании {reservation.id}: {str(e)}")
                    logger.error(f"Тип ошибки: {type(e).__name__}")
                    logger.error(f"Детали ошибки: {e}")
                    messages.warning(request, 'Бронирование создано, но уведомление администратору не отправлено. Обратитесь к администратору.')
                    # Не прерываем выполнение, даже если отправка не удалась
                
                messages.success(request, 'Бронирование успешно создано!')
                return redirect('reservation_success')
            except Exception as e:
                logger.error(f"Ошибка при сохранении бронирования: {str(e)}")
                messages.error(request, 'Произошла ошибка при создании бронирования. Пожалуйста, попробуйте позже.')
        else:
            logger.warning(f"Ошибки валидации формы бронирования: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Ошибка в поле {field}: {error}')
    else:
        form = ReservationForm()
        if request.user.is_authenticated:
            form.initial = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email
            }
    
    return render(request, 'reservation.html', {
        'form': form,
        'user_reservations': user_reservations,
        'today': today
    })

@login_required(login_url='login')
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == 'POST':
        try:
            # Если статус был 'accepted', отправляем уведомление админу
            if reservation.status == 'accepted':
                subject = 'Бронирование отменено пользователем'
                message = f'''
                Пользователь отменил бронирование:
                Имя: {reservation.name}
                Email: {reservation.email}
                Телефон: {reservation.phone}
                Дата: {reservation.date}
                Время: {reservation.time}
                Количество гостей: {reservation.guests}
                '''
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.ADMIN_EMAIL],
                        fail_silently=False,
                    )
                    messages.success(request, 'Уведомление об отмене бронирования отправлено администратору!')
                except Exception as e:
                    logger.error(f"Ошибка при отправке уведомления об отмене бронирования: {str(e)}")
                    messages.warning(request, 'Бронирование отменено, но уведомление администратору не отправлено.')
            reservation.delete()
            messages.success(request, 'Бронирование успешно удалено!')
        except Exception as e:
            logger.error(f"Ошибка при удалении бронирования: {str(e)}")
            messages.error(request, 'Произошла ошибка при удалении бронирования.')
    return redirect('reservation')

def reservation_success(request):
    return render(request, 'reservation_success.html')

def menu_view(request):
    menu_items = MenuItem.objects.filter(is_active=True)
    menu_photos = MenuPhoto.objects.all()
    return render(request, 'menu.html', {'menu_items': menu_items, 'menu_photos': menu_photos})

def news_list(request):
    news = News.objects.all()
    return render(request, 'news.html', {'news': news})

def news_detail(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news_item': news_item})

def test_email(request):
    try:
        logger.info("Начинаем тестирование отправки email")
        logger.info(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        logger.info(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        logger.info(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        logger.info(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
        logger.info(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        logger.info(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
        logger.info(f"ADMIN_EMAIL: {settings.ADMIN_EMAIL}")
        
        send_mail(
            'Тестовое письмо',
            'Это тестовое письмо для проверки настроек email.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        logger.info("Тестовое письмо успешно отправлено")
        return JsonResponse({'status': 'success', 'message': 'Тестовое письмо отправлено'})
    except Exception as e:
        logger.error(f"Ошибка при отправке тестового письма: {str(e)}")
        logger.error(f"Тип ошибки: {type(e).__name__}")
        logger.error(f"Детали ошибки: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)})

def test_email_page(request):
    """Страница для тестирования email настроек"""
    context = {
        'email_host': settings.EMAIL_HOST,
        'email_port': settings.EMAIL_PORT,
        'email_user': settings.EMAIL_HOST_USER,
        'email_ssl': settings.EMAIL_USE_SSL,
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'admin_email': settings.ADMIN_EMAIL,
    }
    return render(request, 'test_email.html', context)

def gallery_view(request):
    photos_interior = MenuPhoto.objects.filter(category='interior').order_by('-created_at')
    photos_dish = MenuPhoto.objects.filter(category='dish').order_by('-created_at')
    return render(request, 'gallery.html', {
        'photos_interior': photos_interior,
        'photos_dish': photos_dish,
    })

def gallery(request):
    interior_photos = GalleryPhoto.objects.filter(category='interior')
    dish_photos = GalleryPhoto.objects.filter(category='dish')
    return render(request, 'gallery.html', {
        'interior_photos': interior_photos,
        'dish_photos': dish_photos,
    })
