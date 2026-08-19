#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ключевая ставка Банка России: официальный SOAP-сервис DailyInfo.

Метод KeyRateXML(fromDate, ToDate) возвращает ставку по дням
(выходные и праздники отсутствуют — ставка переносится с последнего
рабочего дня). WSDL: https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL

Кэш: tmp/keyrate_cache.json — повторные расчёты работают без сети.
Запрос идёт в обход прокси-переменных окружения (socks-прокси не
поддерживается urllib).
"""

import bisect
import calendar
import json
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path

CACHE_PATH = Path(__file__).resolve().parent.parent / "tmp" / "keyrate_cache.json"
SOAP_URL = "https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx"
SOAP_ACTION = "http://web.cbr.ru/KeyRateXML"
SOAP_TMPL = (
    '<?xml version="1.0" encoding="utf-8"?>'
    '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">'
    '<soap:Body><KeyRateXML xmlns="http://web.cbr.ru/">'
    "<fromDate>{from_date}T00:00:00</fromDate>"
    "<ToDate>{to_date}T00:00:00</ToDate>"
    "</KeyRateXML></soap:Body></soap:Envelope>"
)


class CbrUnavailableError(RuntimeError):
    """Сервис ЦБ недоступен или вернул непригодный ответ."""


def _iso(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def _parse_iso(s: str) -> date:
    return date.fromisoformat(s)


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"ranges": [], "days": {}}


def _save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


def _covered(ranges: list, start: date, end: date) -> bool:
    """Покрывает ли объединение закэшированных диапазонов [start, end]."""
    merged = []
    for s, e in sorted(ranges):
        s, e = _parse_iso(s), _parse_iso(e)
        if merged and s <= merged[-1][1] + timedelta(days=1):
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return any(s <= start and end <= e for s, e in merged)


def _fetch_range(start: date, end: date) -> dict:
    """POST к DailyInfo; возвращает {iso_date: ставка}."""
    body = SOAP_TMPL.format(from_date=_iso(start), to_date=_iso(end)).encode("utf-8")
    req = urllib.request.Request(
        SOAP_URL, data=body,
        headers={"Content-Type": "text/xml; charset=utf-8", "SOAPAction": SOAP_ACTION},
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=30) as resp:
            xml = resp.read().decode("utf-8")
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        raise CbrUnavailableError(f"сеть недоступна: {e}") from e

    days = {}
    try:
        root = ET.fromstring(xml)
        for kr in root.iter():
            if not kr.tag.endswith("KR"):
                continue
            dt = rate = None
            for child in kr:
                if child.tag.endswith("DT"):
                    dt = (child.text or "")[:10]
                elif child.tag.endswith("Rate"):
                    rate = float((child.text or "0").replace(",", "."))
            if dt and rate is not None:
                days[dt] = rate
    except ET.ParseError as e:
        raise CbrUnavailableError(f"неожиданный ответ сервиса: {e}") from e
    if not days:
        raise CbrUnavailableError("сервис вернул пустой ответ по ключевой ставке")
    return days


def keyrate_series(start: date, end: date) -> list:
    """[(date, ставка)] на каждый день диапазона включительно.

    Выходные/праздники получают ставку последнего рабочего дня.
    При отсутствии данных в кэше делает запрос к ЦБ и обновляет кэш.
    """
    if end < start:
        raise ValueError("конечная дата меньше начальной")
    cache = _load_cache()
    if not _covered(cache["ranges"], start, end):
        # Буфер 14 дней: для праздников/выходных в начале диапазона
        # ставка берётся с последнего рабочего дня, который может быть раньше start.
        cache["days"].update(_fetch_range(start - timedelta(days=14), end))
        cache["ranges"].append([_iso(start - timedelta(days=14)), _iso(end)])
        _save_cache(cache)

    known = sorted(cache["days"])
    series = []
    for i in range((end - start).days + 1):
        day = start + timedelta(days=i)
        iso = _iso(day)
        idx = bisect.bisect_left(known, iso)
        if idx < len(known) and known[idx] == iso:
            rate = cache["days"][iso]
        else:
            if idx == 0:
                raise CbrUnavailableError(f"нет ставки ЦБ на {iso} и ранее")
            rate = cache["days"][known[idx - 1]]
        series.append((day, rate))
    return series


def days_in_year(year: int) -> int:
    return 366 if calendar.isleap(year) else 365
