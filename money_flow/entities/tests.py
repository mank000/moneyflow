from datetime import date, timedelta
from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, MoneyFlow, Status, SubCategory, Type


class BaseTestCase(TestCase):
    """Базовый класс с фикстурами для всех тестов."""

    def setUp(self):
        self.client = Client()

        self.type_income = Type.objects.create(name="Доход")
        self.type_expense = Type.objects.create(name="Расход")

        self.category = Category.objects.create(
            name="Зарплата", type=self.type_income
        )
        self.category_expense = Category.objects.create(
            name="Еда", type=self.type_expense
        )

        self.subcategory = SubCategory.objects.create(
            name="Основная зарплата", category=self.category
        )
        self.subcategory_expense = SubCategory.objects.create(
            name="Рестораны", category=self.category_expense
        )

        self.status_done = Status.objects.create(name="Выполнено")
        self.status_pending = Status.objects.create(name="В ожидании")

        self.flow = MoneyFlow.objects.create(
            type=self.type_income,
            category=self.category,
            sub_category=self.subcategory,
            status=self.status_done,
            total=Decimal("50000.00"),
            date_of_creation=date.today(),
            description="Зарплата за июнь",
        )


class MoneyFlowCRUDTest(BaseTestCase):
    """Тест 1: Полный CRUD-цикл MoneyFlow."""

    def test_full_crud_lifecycle(self):
        # CREATE
        response = self.client.post(
            reverse("entities:moneyflow_create"),
            data={
                "type": self.type_expense.pk,
                "category": self.category_expense.pk,
                "sub_category": self.subcategory_expense.pk,
                "status": self.status_pending.pk,
                "total": "1500.00",
                "date_of_creation": date.today().isoformat(),
                "description": "Ужин",
            },
        )
        self.assertEqual(response.status_code, 302)
        new_flow = MoneyFlow.objects.get(description="Ужин")
        self.assertEqual(new_flow.total, Decimal("1500.00"))

        # READ
        response = self.client.get(reverse("entities:moneyflow_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(new_flow, response.context["flows"])

        # UPDATE
        response = self.client.post(
            reverse("entities:moneyflow_update", kwargs={"pk": new_flow.pk}),
            data={
                "type": self.type_expense.pk,
                "category": self.category_expense.pk,
                "sub_category": self.subcategory_expense.pk,
                "status": self.status_done.pk,
                "total": "2000.00",
                "date_of_creation": date.today().isoformat(),
                "description": "Ужин (обновлено)",
            },
        )
        self.assertEqual(response.status_code, 302)
        new_flow.refresh_from_db()
        self.assertEqual(new_flow.total, Decimal("2000.00"))
        self.assertEqual(new_flow.description, "Ужин (обновлено)")

        # DELETE
        response = self.client.post(
            reverse("entities:moneyflow_delete", kwargs={"pk": new_flow.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MoneyFlow.objects.filter(pk=new_flow.pk).exists())


class MoneyFlowFilterByTypeTest(BaseTestCase):
    """Тест 2: Фильтрация денежных потоков по типу."""

    def test_filter_by_type(self):
        MoneyFlow.objects.create(
            type=self.type_expense,
            category=self.category_expense,
            sub_category=self.subcategory_expense,
            status=self.status_done,
            total=Decimal("3000.00"),
            date_of_creation=date.today(),
            description="Расход на еду",
        )

        response = self.client.get(
            reverse("entities:moneyflow_list"),
            {"type": self.type_income.pk},
        )
        flows = response.context["flows"]
        self.assertTrue(all(f.type == self.type_income for f in flows))
        self.assertEqual(flows.count(), 1)

        response = self.client.get(
            reverse("entities:moneyflow_list"),
            {"type": self.type_expense.pk},
        )
        flows = response.context["flows"]
        self.assertTrue(all(f.type == self.type_expense for f in flows))
        self.assertEqual(flows.count(), 1)


class MoneyFlowFilterByDateRangeTest(BaseTestCase):
    """Тест 3: Фильтрация по диапазону дат."""

    def test_filter_by_date_range(self):
        old_flow = MoneyFlow.objects.create(
            type=self.type_income,
            category=self.category,
            sub_category=self.subcategory,
            status=self.status_done,
            total=Decimal("10000.00"),
            date_of_creation=date.today() - timedelta(days=30),
            description="Старая запись",
        )
        recent_flow = self.flow

        week_ago = (date.today() - timedelta(days=7)).isoformat()
        today = date.today().isoformat()

        response = self.client.get(
            reverse("entities:moneyflow_list"),
            {"date_from": week_ago, "date_to": today},
        )
        flows = response.context["flows"]
        self.assertIn(recent_flow, flows)
        self.assertNotIn(old_flow, flows)

        month_ago = (date.today() - timedelta(days=31)).isoformat()
        two_weeks_ago = (date.today() - timedelta(days=14)).isoformat()

        response = self.client.get(
            reverse("entities:moneyflow_list"),
            {"date_from": month_ago, "date_to": two_weeks_ago},
        )
        flows = response.context["flows"]
        self.assertIn(old_flow, flows)
        self.assertNotIn(recent_flow, flows)


class MoneyFlowCombinedFiltersTest(BaseTestCase):
    """Тест 4: Комбинация нескольких фильтров одновременно."""

    def test_combined_filters(self):
        matching = MoneyFlow.objects.create(
            type=self.type_expense,
            category=self.category_expense,
            sub_category=self.subcategory_expense,
            status=self.status_pending,
            total=Decimal("500.00"),
            date_of_creation=date.today(),
            description="Целевая запись",
        )

        response = self.client.get(
            reverse("entities:moneyflow_list"),
            {
                "type": self.type_expense.pk,
                "category": self.category_expense.pk,
                "status": self.status_pending.pk,
                "date_from": date.today().isoformat(),
                "date_to": date.today().isoformat(),
            },
        )
        flows = list(response.context["flows"])
        self.assertEqual(len(flows), 1)
        self.assertEqual(flows[0], matching)


class MoneyFlowInlineCreateFromListTest(BaseTestCase):
    """Тест 5: Создание MoneyFlow через POST на list view."""

    def test_create_via_list_post(self):
        initial_count = MoneyFlow.objects.count()

        response = self.client.post(
            reverse("entities:moneyflow_list"),
            data={
                "type": self.type_income.pk,
                "category": self.category.pk,
                "sub_category": self.subcategory.pk,
                "status": self.status_done.pk,
                "total": "99999.00",
                "date_of_creation": date.today().isoformat(),
                "description": "Создано через list view",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MoneyFlow.objects.count(), initial_count + 1)
        self.assertTrue(
            MoneyFlow.objects.filter(
                description="Создано через list view"
            ).exists()
        )


class StatusCRUDTest(BaseTestCase):
    """Тест 6: CRUD-цикл для модели Status."""

    def test_status_crud(self):
        # CREATE
        response = self.client.post(
            reverse("entities:status_create"),
            data={"name": "Отменено"},
        )
        self.assertEqual(response.status_code, 302)
        status = Status.objects.get(name="Отменено")

        # LIST
        response = self.client.get(reverse("entities:status_list"))
        self.assertIn(status, response.context["statuses"])

        # UPDATE
        response = self.client.post(
            reverse("entities:status_update", kwargs={"pk": status.pk}),
            data={"name": "Аннулировано"},
        )
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, "Аннулировано")

        # DELETE
        response = self.client.post(
            reverse("entities:status_delete", kwargs={"pk": status.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())


class CategoryFilterByTypeTest(BaseTestCase):
    """Тест 7: Фильтрация категорий по типу."""

    def test_category_filter_by_type(self):
        response = self.client.get(
            reverse("entities:category_list"),
            {"type": self.type_income.pk},
        )
        categories = response.context["categories"]
        self.assertIn(self.category, categories)
        self.assertNotIn(self.category_expense, categories)
        self.assertEqual(
            response.context["selected_type"], str(self.type_income.pk)
        )

    def test_category_no_filter_returns_all(self):
        response = self.client.get(reverse("entities:category_list"))
        categories = response.context["categories"]
        self.assertEqual(categories.count(), 2)


class SubCategoryFilterByCategoryTest(BaseTestCase):
    """Тест 8: Фильтрация подкатегорий по категории."""

    def test_subcategory_filter(self):
        response = self.client.get(
            reverse("entities:subcategory_list"),
            {"category": self.category.pk},
        )
        subcategories = response.context["subcategories"]
        self.assertIn(self.subcategory, subcategories)
        self.assertNotIn(self.subcategory_expense, subcategories)

    def test_subcategory_context_has_categories(self):
        response = self.client.get(reverse("entities:subcategory_list"))
        self.assertIn("categories", response.context)
        self.assertEqual(response.context["categories"].count(), 2)


class TypeCRUDWithCascadeContextTest(BaseTestCase):
    """Тест 9: CRUD типа + проверка контекста UpdateView."""

    def test_type_create_and_update_context(self):
        # CREATE
        response = self.client.post(
            reverse("entities:type_create"),
            data={"name": "Инвестиции"},
        )
        self.assertEqual(response.status_code, 302)
        new_type = Type.objects.get(name="Инвестиции")

        # UPDATE — GET для проверки контекста
        response = self.client.get(
            reverse("entities:type_update", kwargs={"pk": new_type.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flow"], new_type)

        # DELETE
        response = self.client.post(
            reverse("entities:type_delete", kwargs={"pk": new_type.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Type.objects.filter(name="Инвестиции").exists())


class MainPageAndInvalidFormTest(BaseTestCase):
    """Тест 10: Главная страница + невалидные формы."""

    def test_main_page_renders(self):
        response = self.client.get(reverse("entities:moneyflow_list"))
        self.assertEqual(response.status_code, 200)

    def test_invalid_moneyflow_form_returns_errors(self):
        response = self.client.post(
            reverse("entities:moneyflow_create"),
            data={},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())
        self.assertGreater(len(response.context["form"].errors), 0)

    def test_invalid_inline_form_on_list(self):
        """POST с невалидными данными на list view не создаёт объект."""
        initial_count = MoneyFlow.objects.count()
        response = self.client.post(
            reverse("entities:moneyflow_list"),
            data={"total": "not_a_number"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MoneyFlow.objects.count(), initial_count)
