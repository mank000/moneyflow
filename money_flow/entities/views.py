from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from . import forms
from .models import Category, MoneyFlow, Status, SubCategory, Type


# Crud для модели денежного потока
class MoneyFlowCreateView(CreateView):
    model = MoneyFlow
    form_class = forms.MoneyFlowForm
    template_name = "moneyflow/moneyflow_create.html"
    success_url = reverse_lazy("entities:moneyflow_list")


class MoneyFlowUpdateView(UpdateView):
    model = MoneyFlow
    form_class = forms.MoneyFlowForm
    template_name = "moneyflow/moneyflow_create.html"
    success_url = reverse_lazy("entities:moneyflow_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flow"] = self.get_object()
        return context


class MoneyFlowDeleteView(DeleteView):
    model = MoneyFlow
    template_name = "moneyflow/moneyflow_delete.html"
    success_url = reverse_lazy("entities:moneyflow_list")


class MoneyFlowTableView(FormMixin, ListView):
    model = MoneyFlow
    template_name = "moneyflow/moneyflow_list.html"
    context_object_name = "flows"
    form_class = forms.MoneyFlowForm

    def get_queryset(self):
        queryset = MoneyFlow.objects.select_related(
            "type", "category", "sub_category", "status"
        ).order_by("-date_of_creation")

        type_id = self.request.GET.get("type")
        category_id = self.request.GET.get("category")
        status_id = self.request.GET.get("status")
        date_from = parse_date(self.request.GET.get("date_from", ""))
        date_to = parse_date(self.request.GET.get("date_to", ""))

        if type_id:
            queryset = queryset.filter(type_id=type_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if date_from:
            queryset = queryset.filter(date_of_creation__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_of_creation__lte=date_to)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["types"] = Type.objects.all()
        context["categories"] = Category.objects.all()
        context["statuses"] = Status.objects.all()
        context["date_from"] = self.request.GET.get("date_from", "")
        context["date_to"] = self.request.GET.get("date_to", "")
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("entities:moneyflow_list")


# Crud для модели статуса
class StatusTableView(ListView):
    model = Status
    template_name = "status/status_list.html"
    context_object_name = "statuses"


class StatusDeleteView(DeleteView):
    model = Status
    template_name = "status/status_delete.html"
    success_url = reverse_lazy("entities:status_list")


class StatusUpdateView(UpdateView):
    model = Status
    form_class = forms.StatusFlowForm
    template_name = "status/status_create.html"
    success_url = reverse_lazy("entities:status_list")


class StatusCreateView(CreateView):
    model = Status
    form_class = forms.StatusFlowForm
    template_name = "status/status_create.html"
    success_url = reverse_lazy("entities:status_list")


# CRUD для модели типа
class TypeCreateView(CreateView):
    model = Type
    form_class = forms.TypeForm
    template_name = "type/type_create.html"
    success_url = reverse_lazy("entities:type_list")


class TypeUpdateView(UpdateView):
    model = Type
    form_class = forms.TypeForm
    template_name = "type/type_create.html"
    success_url = reverse_lazy("entities:type_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flow"] = self.get_object()
        return context


class TypeDeleteView(DeleteView):
    model = Type
    template_name = "type/type_delete.html"
    success_url = reverse_lazy("entities:type_list")


class TypeTableView(ListView):
    model = Type
    template_name = "type/type_list.html"
    context_object_name = "types"


# CRUD для модели категории
class CategoryCreateView(CreateView):
    model = Category
    form_class = forms.CategoryForm
    template_name = "category/category_create.html"
    success_url = reverse_lazy("entities:category_list")


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = forms.CategoryForm
    template_name = "category/category_create.html"
    success_url = reverse_lazy("entities:category_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flow"] = self.get_object()
        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category/category_delete.html"
    success_url = reverse_lazy("entities:category_list")


class CategoryTableView(ListView):
    model = Category
    template_name = "category/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        queryset = Category.objects.select_related("type").order_by("id")
        type_id = self.request.GET.get("type")
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = Type.objects.all()
        context["selected_type"] = self.request.GET.get("type", "")
        return context


# CRUD для подкатегории
class SubCategoryCreateView(CreateView):
    model = SubCategory
    form_class = forms.SubCategoryForm
    template_name = "subcategory/subcategory_create.html"
    success_url = reverse_lazy("entities:subcategory_list")


class SubCategoryUpdateView(UpdateView):
    model = SubCategory
    form_class = forms.SubCategoryForm
    template_name = "subcategory/subcategory_create.html"
    success_url = reverse_lazy("entities:subcategory_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["flow"] = self.get_object()
        return context


class SubCategoryDeleteView(DeleteView):
    model = SubCategory
    template_name = "subcategory/subcategory_delete.html"
    success_url = reverse_lazy("entities:subcategory_list")


class SubCategoryTableView(ListView):
    model = SubCategory
    template_name = "subcategory/subcategory_list.html"
    context_object_name = "subcategories"

    def get_queryset(self):
        queryset = SubCategory.objects.select_related("category").order_by(
            "id"
        )
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected_category"] = self.request.GET.get("category", "")
        return context


def main_page(request):
    return render(request, "base.html")
