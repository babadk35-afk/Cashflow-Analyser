#!/usr/bin/env python3
import random
from typing import List, Dict

class Transaction:
    def __init__(self, date: str, amount: float, category: str):
        self.date = date
        self.amount = amount
        self.category = category

class CashFlowAnalyzer:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self, date: str, amount: float, category: str):
        self.transactions.append(Transaction(date, amount, category))

    def net_cash_flow(self) -> float:
        return sum(t.amount for t in self.transactions)

    def cumulative_balance(self) -> List[float]:
        balance = []
        total = 0.0
        for t in self.transactions:
            total += t.amount
            balance.append(total)
        return balance

    def category_summary(self) -> Dict[str, float]:
        summary: Dict[str, float] = {}
        for t in self.transactions:
            summary[t.category] = summary.get(t.category, 0.0) + t.amount
        return summary

    def average_cash_flow(self) -> float:
        if not self.transactions:
            return 0.0
        return sum(t.amount for t in self.transactions) / len(self.transactions)

    def max_cash_inflow(self) -> float:
        inflows = [t.amount for t in self.transactions if t.amount > 0]
        return max(inflows) if inflows else 0.0

    def max_cash_outflow(self) -> float:
        outflows = [t.amount for t in self.transactions if t.amount < 0]
        return min(outflows) if outflows else 0.0

def demo():
    analyzer = CashFlowAnalyzer()
    categories = ["Salary", "Rent", "Food", "Investment", "Entertainment"]
    for i in range(30):
        date = f"2025-10-{i+1:02d}"
        amount = random.uniform(-200, 500)
        category = random.choice(categories)
        analyzer.add_transaction(date, amount, category)

    print("Net Cash Flow:", round(analyzer.net_cash_flow(),2))
    print("Cumulative Balance:", [round(b,2) for b in analyzer.cumulative_balance()])
    print("Category Summary:", {k: round(v,2) for k,v in analyzer.category_summary().items()})
    print("Average Cash Flow:", round(analyzer.average_cash_flow(),2))
    print("Max Inflow:", round(analyzer.max_cash_inflow(),2))
    print("Max Outflow:", round(analyzer.max_cash_outflow(),2))

if __name__ == "__main__":
    demo()
