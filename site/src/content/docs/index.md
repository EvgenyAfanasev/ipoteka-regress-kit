---
title: Главная
description: Взыскание 1/2 ипотечных платежей с бывшего супруга в порядке регресса — стратегия и генераторы документов
template: splash
hero:
  title: ipoteka-regress-kit
  tagline: >-
    Взыскание с бывшего супруга 1/2 доли платежей по ипотечному кредиту в
    порядке регресса (п. 2 ст. 325 ГК РФ) — юридическая стратегия, генераторы
    досудебной претензии и искового заявления, автоматический расчёт
    процентов по ст. 395 ГК РФ и госпошлины.
  actions:
    - text: Читать план стратегии
      link: /plan/
      icon: right-arrow
      variant: primary
    - text: GitHub
      link: https://github.com/EvgenyAfanasev/ipoteka-regress-kit
      icon: external
      variant: minimal
---

## Что это

Квартира куплена в браке в ипотеку, оба супруга — созаёмщики с солидарной
ответственностью. Развод оформлен, раздела имущества не было, платит один —
и хочет вернуть половину. Этот набор — пошаговый план и инструменты для такой
ситуации.

- **План стратегии** — правовой каркас, этапы от претензии до ФССП, сроки,
  шаблоны документов, чек-листы;
- **Генераторы документов** — досудебная претензия и исковое заявление
  в формате docx: интерактивный ввод, профиль данных в `.env`;
- **Автоматические расчёты** — проценты по ст. 395 ГК РФ по ключевой
  ставке ЦБ (посуточно, с учётом смен ставки), госпошлина по
  ст. 333.19 НК РФ, проверка подсудности.

> ⚠️ Инструмент и конспект стратегии, а не юридическая консультация.
> Нормы и пороги меняются — сверяйте с действующими редакциями.

## Скачать скрипты

Требуется Python 3.10+ и `pip install -r requirements.txt`
(единственная зависимость — `python-docx`).

```bash
base=https://raw.githubusercontent.com/EvgenyAfanasev/ipoteka-regress-kit/master
curl -O $base/scripts/pretenziya.py -O $base/scripts/isk.py \
     -O $base/scripts/cbr_rate.py -O $base/requirements.txt
```

| Файл | Что делает |
|---|---|
| [pretenziya.py](https://raw.githubusercontent.com/EvgenyAfanasev/ipoteka-regress-kit/master/scripts/pretenziya.py) | досудебная претензия → docx |
| [isk.py](https://raw.githubusercontent.com/EvgenyAfanasev/ipoteka-regress-kit/master/scripts/isk.py) | исковое заявление → docx (проценты, пошлина, подсудность) |
| [cbr_rate.py](https://raw.githubusercontent.com/EvgenyAfanasev/ipoteka-regress-kit/master/scripts/cbr_rate.py) | ключевая ставка ЦБ (SOAP, кэш, офлайн-режим) |
| [requirements.txt](https://raw.githubusercontent.com/EvgenyAfanasev/ipoteka-regress-kit/master/requirements.txt) | зависимости (`python-docx`) |

## Быстрый старт

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/python pretenziya.py --init   # создать .env из .env.example
$EDITOR .env                             # заполнить постоянные данные

.venv/bin/python pretenziya.py           # досудебная претензия -> docx
.venv/bin/python isk.py                  # исковое заявление -> docx
```

Подробности: [план стратегии](/plan/) и
[README репозитория](https://github.com/EvgenyAfanasev/ipoteka-regress-kit#readme).
