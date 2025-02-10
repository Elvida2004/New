from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserAbstract, Request

admin.site.register(UserAbstract)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'get_full_name', 'address', 'phone', 'email',
        'request_date', 'service', 'preferred_payment_method', 'status', 'cancel_reason'
    ]
    list_filter = ('status', 'service', 'preferred_payment_method')  # Фильтрация
    search_fields = ('user__username', 'user__full_name', 'email', 'phone', 'address')  # Поиск
    ordering = ('id',)  # Сортировка по ID (по возрастанию)

    def get_full_name(self, obj):
        return obj.user.full_name  # Получаем ФИО пользователя

    get_full_name.short_description = "ФИО"  # Название колонки в админке