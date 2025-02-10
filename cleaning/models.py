from django.db import models
from django.contrib.auth.models import AbstractUser


class UserAbstract(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    def __str__(self):
        return self.username


# Модель для заявки
class Request(models.Model):
    SERVICE_CHOICES = [
        ('general', 'Общий клининг'),
        ('deep', 'Генеральная уборка'),
        ('construction', 'Послестроительная уборка'),
        ('dry_cleaning', 'Химчистка ковров и мебели'),
    ]
    STATUS_CHOICES = [
        ('new', 'Новая заявка'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Наличные'),
        ('card', 'Банковская карта'),
    ]

    user = models.ForeignKey(UserAbstract, on_delete=models.CASCADE, verbose_name="Пользователь")  # Связь с пользователем

    address = models.TextField(verbose_name="Адрес")  # Адрес для заявки
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")  # Email для связи
    request_date = models.DateTimeField(verbose_name="Дата и время")  # Дата и время для услуги
    service = models.CharField(max_length=255, choices=SERVICE_CHOICES, verbose_name="Тип услуги")  # Статический список услуг
    preferred_payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, default='cash', verbose_name="Тип оплаты"
    )  # Тип оплаты
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")  # Статус заявки
    cancel_reason = models.TextField(null=True, blank=True, verbose_name="Причина отмены")  # Причина отмены, если заявка отменена

    def __str__(self):
        return f"Заявка {self.id} от {self.user.username}"

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
