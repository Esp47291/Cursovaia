
from src.services import investment_bank

TRANSACTIONS = [
    {"Дата операции": "2023-12-05", "Сумма операции": 101.0},
    {"Дата операции": "2023-12-10", "Сумма операции": 249.0},
]

def test_investment_bank():
    saved = investment_bank("2023-12", TRANSACTIONS, 50)
    assert abs(saved - ( (150-101)+(250-249) )) < 1e-6
