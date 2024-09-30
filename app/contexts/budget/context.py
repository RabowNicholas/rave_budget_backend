from datetime import datetime
from enum import Enum

from app.contexts.budget.models import Budget, BudgetExpense, BudgetLimit
from app.contexts.budget.repository import BudgetRepository


class BudgetDataEnum(Enum):
    TICKETS = "tickets"
    TRAVEL = "travel"
    ACCOMMODATION = "accommodation"
    FOOD = "food"
    OTHER = "other"


class BudgetOverviewData:
    name: str
    date: datetime
    location: str


class BudgetLimitData:
    category: BudgetDataEnum
    amount: float


class BudgetData:
    overview: BudgetOverviewData
    limits: list[BudgetLimitData]


class BudgetNotFoundException(Exception):
    pass


class BudgetContext:
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def create_budget(self, user_id: str, data: BudgetData) -> Budget:
        budget = self._prepare_budget(user_id=user_id, data=data)
        return self.repository.save_budget(budget)

    def get_budget(self, budget_id: str) -> Budget:

        budget = self.repository.get_budget_by_id(budget_id)
        if not budget:
            raise BudgetNotFoundException("Budget not found")
        return budget

    def get_budgets_for_user(self, user_id: str) -> list[Budget]:
        return self.repository.get_budgets_for_user_id(user_id)

    def add_expense(
        self, budget_id: str, amount: float, category: str
    ) -> BudgetExpense:
        e = BudgetExpense(
            budget_id=budget_id,
            amount=amount,
            category=category,
        )
        return self.repository.save_expense(e)

    def _prepare_budget(self, user_id: str, data: BudgetData) -> Budget:
        budget = Budget(
            user_id=user_id,
            name=data.overview.name,
            date=data.overview.date,
            location=data.overview.location,
        )

        for limit_data in data.limits:
            budget_limit = BudgetLimit(
                category=limit_data.category,
                amount=limit_data.amount,
                budget_id=budget.id,
            )
            budget.limits.append(budget_limit)

        return budget
