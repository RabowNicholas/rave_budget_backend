from sqlalchemy.orm import Session

from app.contexts.budget.models import Budget, BudgetExpense, BudgetLimit


class BudgetRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_budget(self, budget: Budget) -> Budget:
        self.session.add(budget)

        for limit in budget.limits:
            self.session.add(limit)

        self.session.commit()

        return budget

    def get_budget_by_id(self, budget_id: str) -> Budget | None:
        return self.session.query(Budget).filter(Budget.id == budget_id).one()

    def get_budgets_for_user_id(self, user_id: str) -> list[Budget]:
        return self.session.query(Budget).filter(Budget.user_id == user_id).all()

    def save_expense(self, budget_expense: BudgetExpense) -> BudgetExpense:
        self.session.add(budget_expense)
        self.session.commit()
        return budget_expense
