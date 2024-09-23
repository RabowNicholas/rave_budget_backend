from sqlalchemy.orm import Session

from app.contexts.budget.models import Budget


class BudgetRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_budget(self, budget: Budget) -> Budget:
        self.session.add(budget)
        self.session.commit()
        return budget
