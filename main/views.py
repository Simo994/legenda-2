from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import ReservationForm, UserRegisterForm, FeedbackForm
import logging
import json
from django.contrib.auth.forms import UserCreationForm
from .models import MenuItem, MenuPhoto, Reservation
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
    user_reservations = Reservation.objects.filter(email=request.user.email).order_by('-date', '-time')
    today = date.today()
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.save()
                messages.success(request, 'Бронирование успешно создано!')
                return redirect('reservation')
            except Exception as e:
                logger.error(f"Ошибка при сохранении бронирования: {str(e)}")
                messages.error(request, 'Произошла ошибка при создании бронирования. Пожалуйста, попробуйте позже.')
        else:
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
    reservation = get_object_or_404(Reservation, id=reservation_id, email=request.user.email)
    if request.method == 'POST':
        try:
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
