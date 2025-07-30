# forms.py
from django import forms

from .models import Category, MoneyFlow, Status, SubCategory, Type


class MoneyFlowForm(forms.ModelForm):
    """Форма для создания/обновления денежного потока."""

    class Meta:
        model = MoneyFlow
        fields = [
            "status",
            "type",
            "category",
            "sub_category",
            "total",
            "description",
            "date_of_creation",
        ]
        widgets = {
            "date_of_creation": forms.DateInput(attrs={"type": "date"}),
        }


class StatusFlowForm(forms.ModelForm):
    """Форма для создания/изменения статуса."""

    class Meta:
        model = Status
        fields = ["name"]


class TypeForm(forms.ModelForm):
    """Форма для создания/изменения типа."""

    class Meta:
        model = Type
        fields = ["name"]


class CategoryForm(forms.ModelForm):
    """Форма для создания/изменения категории."""

    class Meta:
        model = Category
        fields = ["name", "type"]


class SubCategoryForm(forms.ModelForm):
    """Форма для создания/изменения подкатегории."""

    class Meta:
        model = SubCategory
        fields = ["name", "category"]
