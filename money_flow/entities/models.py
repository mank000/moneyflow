from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now
from smart_selects.db_fields import ChainedForeignKey


class MoneyFlow(models.Model):
    """Модель для денежного потока."""

    date_of_creation = models.DateField("Дата создания", default=now)
    status = models.ForeignKey(
        "Status",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Статус",
    )
    type = models.ForeignKey(
        "Type",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name="Тип",
    )
    category = ChainedForeignKey(
        "Category",
        chained_field="type",
        chained_model_field="type",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=False,
        blank=False,
        verbose_name="Категория",
    )

    sub_category = ChainedForeignKey(
        "SubCategory",
        chained_field="category",
        chained_model_field="category",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=False,
        blank=False,
        verbose_name="Подкатегория",
    )

    total = models.DecimalField(
        "Сумма(в рублях)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    description = models.TextField("Комментарий", blank=True)

    class Meta:
        verbose_name = "Денежный поток"
        verbose_name_plural = "Денежные потоки"


class Status(models.Model):
    """Модель для возможности выбора статуса."""

    name = models.CharField(
        max_length=32, unique=True, verbose_name="Статус", blank=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Type(models.Model):
    """Модель для возможности выбора типа."""

    name = models.CharField(
        max_length=32, unique=True, verbose_name="Тип", blank=False
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Category(models.Model):
    """Модель для категорий."""

    name = models.CharField(
        max_length=32, unique=True, verbose_name="Категория", blank=False
    )
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE, verbose_name="Категория"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    """Модель для подкатегорий."""

    name = models.CharField(
        max_length=32, unique=True, verbose_name="Подкатегория", blank=False
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
