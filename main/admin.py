from django.contrib import admin
from .models import Reservation, Feedback, MenuItem, MenuPhoto, News
from django.utils import timezone

# Register your models here.

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'date', 'time', 'guests', 'status', 'created_at')
    list_filter = ('status', 'date', 'created_at')
    search_fields = ('name', 'phone', 'email')
    ordering = ('-created_at',)
    actions = ['accept_reservations', 'reject_reservations']
    
    def accept_reservations(self, request, queryset):
        queryset.update(status='accepted')
    accept_reservations.short_description = "Принять выбранные бронирования"
    
    def reject_reservations(self, request, queryset):
        queryset.update(status='rejected')
    reject_reservations.short_description = "Отклонить выбранные бронирования"

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'subject', 'created_at', 'is_read')
    list_filter = ('created_at', 'is_read')
    search_fields = ('name', 'phone', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def save_model(self, request, obj, form, change):
        if change and 'is_read' in form.changed_data:
            # Если сообщение помечено как прочитанное
            if obj.is_read:
                obj.read_by = request.user
                obj.read_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'price')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'price', 'image')
        }),
        ('Статус', {
            'fields': ('is_active',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MenuPhoto)
class MenuPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created_at')
    readonly_fields = ('created_at',)
    search_fields = ('description',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'content')
    date_hierarchy = 'date'
