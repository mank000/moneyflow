from django.contrib import admin
from django.contrib.auth.models import Group, User
from rangefilter.filters import DateRangeFilter

from .models import Category, MoneyFlow, Status, SubCategory, Type

admin.site.unregister(User)
admin.site.unregister(Group)


class TypeInline(admin.StackedInline):
    model = Type
    extra = 0


class MoneyFlowAdmin(admin.ModelAdmin):
    """Админка для денежного потока."""

    list_display = (
        "date_of_creation",
        "status",
        "type",
        "category",
        "sub_category",
        "total",
        "short_description",
    )
    list_filter = (
        ("date_of_creation", DateRangeFilter),
        "status",
        "type__name",
        "category__name",
        "sub_category__name",
    )

    def short_description(self, obj):
        """Возвращает первые 40 символов поля description."""
        if obj.description:
            return (
                (obj.description[:40] + "...")
                if len(obj.description) > 40
                else obj.description
            )
        return "—"

    short_description.short_description = "Комментарий"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Фильтрация подкатегорий по выбранной категории."""
        if db_field.name == "sub_category":
            if request.resolver_match:
                object_id = request.resolver_match.kwargs.get("object_id")
                if object_id:
                    try:
                        obj = MoneyFlow.objects.get(pk=object_id)
                        if obj.category:
                            kwargs["queryset"] = SubCategory.objects.filter(
                                category=obj.category
                            )
                    except MoneyFlow.DoesNotExist:
                        pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryAdmin(admin.ModelAdmin):
    """Модель для админки категорий."""

    list_display = (
        "name",
        "type__name",
    )
    list_filter = ("type__name",)


class SubCategoryAdmin(admin.ModelAdmin):
    """Модель для админки подкатегорий."""

    list_display = ("name", "category__name")
    list_filter = ("category__name",)


admin.site.register(MoneyFlow, MoneyFlowAdmin)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
