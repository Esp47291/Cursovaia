
from __future__ import annotations

import json
import math
import re
from datetime import datetime
from typing import List, Dict, Any, Callable

from .logger import logger

# ---------------- Общие ----------------
def _jsonify(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2)

# ---------------- Простой поиск ----------------
def simple_search(query: str, transactions: List[Dict[str, Any]]) -> str:
    """Return transactions whose *query* substring appears in description or category."""
    q = query.lower()
    filtered = [t for t in transactions if q in str(t.get("Описание", "")).lower() or q in str(t.get("Категория", "")).lower()]
    logger.info("Simple search for '%s': %d results", query, len(filtered))
    return _jsonify(filtered)

# ---------------- Инвесткопилка ----------------
def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Return rounded savings for *month* and *limit* (10, 50, 100)."""
    try:
        period = datetime.strptime(month, "%Y-%m")
    except ValueError as exc:
        raise ValueError("month must be in 'YYYY-MM' format") from exc

    if limit not in (10, 50, 100):
        raise ValueError("limit must be 10, 50 or 100")

    total_saved = 0.0
    for t in transactions:
        op_date = datetime.strptime(str(t["Дата операции"]), "%Y-%m-%d")
        if op_date.year == period.year and op_date.month == period.month:
            amount = float(t["Сумма операции"])
            rounded = math.ceil(amount / limit) * limit
            total_saved += rounded - amount
    logger.info("Investment bank calculated: %.2f", total_saved)
    return round(total_saved, 2)

# ---------------- Поиск по телефону ----------------
PHONE_RE = re.compile(r"(\+7\s?\d{3}\s?\d{3}[-\s]?\d{2}[-\s]?\d{2})")

def phone_search(transactions: List[Dict[str, Any]]) -> str:
    matched = [t for t in transactions if PHONE_RE.search(str(t.get("Описание", "")))]
    logger.info("Phone search: %d matches", len(matched))
    return _jsonify(matched)

# ---------------- Поиск переводов физлицам ----------------
PERSON_RE = re.compile(r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.?$")

def people_transfer_search(transactions: List[Dict[str, Any]]) -> str:
    matched = [
        t
        for t in transactions
        if t.get("Категория") == "Переводы" and PERSON_RE.search(str(t.get("Описание", "")).strip())
    ]
    logger.info("People transfer search: %d matches", len(matched))
    return _jsonify(matched)
