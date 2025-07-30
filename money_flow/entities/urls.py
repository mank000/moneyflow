from django.urls import include, path

from . import views

app_name = "entities"

moneyflowpatterns = [
    path(
        "create/", views.MoneyFlowCreateView.as_view(), name="moneyflow_create"
    ),
    path(
        "<int:pk>/update/",
        views.MoneyFlowUpdateView.as_view(),
        name="moneyflow_update",
    ),
    path(
        "<int:pk>/delete/",
        views.MoneyFlowDeleteView.as_view(),
        name="moneyflow_delete",
    ),
]

statuspatterns = [
    path("create/", views.StatusCreateView.as_view(), name="status_create"),
    path(
        "<int:pk>/update/",
        views.StatusUpdateView.as_view(),
        name="status_update",
    ),
    path(
        "<int:pk>/delete/",
        views.StatusDeleteView.as_view(),
        name="status_delete",
    ),
    path("", views.StatusTableView.as_view(), name="status_list"),
]


typepatterns = [
    path("create/", views.TypeCreateView.as_view(), name="type_create"),
    path(
        "<int:pk>/update/", views.TypeUpdateView.as_view(), name="type_update"
    ),
    path(
        "<int:pk>/delete/", views.TypeDeleteView.as_view(), name="type_delete"
    ),
    path("", views.TypeTableView.as_view(), name="type_list"),
]


categoriespatterns = [
    path(
        "create/", views.CategoryCreateView.as_view(), name="category_create"
    ),
    path(
        "<int:pk>/update/",
        views.CategoryUpdateView.as_view(),
        name="category_update",
    ),
    path(
        "<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path("", views.CategoryTableView.as_view(), name="category_list"),
]


subcategoriespatterns = [
    path(
        "create/",
        views.SubCategoryCreateView.as_view(),
        name="subcategory_create",
    ),
    path(
        "<int:pk>/update/",
        views.SubCategoryUpdateView.as_view(),
        name="subcategory_update",
    ),
    path(
        "<int:pk>/delete/",
        views.SubCategoryDeleteView.as_view(),
        name="subcategory_delete",
    ),
    path("", views.SubCategoryTableView.as_view(), name="subcategory_list"),
]


urlpatterns = [
    path("", views.MoneyFlowTableView.as_view(), name="moneyflow_list"),
    path("subcategories/", include(subcategoriespatterns)),
    path("categories/", include(categoriespatterns)),
    path("moneyflow/", include(moneyflowpatterns)),
    path("status/", include(statuspatterns)),
    path("type/", include(typepatterns)),
]
