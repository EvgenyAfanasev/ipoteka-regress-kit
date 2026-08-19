# Спека: сайт документации на GitHub Pages (Starlight)

Дата: 2026-08-19 · Статус: на утверждении

## 1. Цель

Публичный сайт по адресу `https://evgenyafanasev.github.io/ipoteka-regress-kit/`:
лендинг с кнопками скачивания скриптов + план стратегии (`docs/plan.md`),
отрендеренный как одна длинная страница с оглавлением и поиском.

## 2. Стек

- **Astro 7 + @astrojs/starlight 0.41** — современная тема документации; из коробки:
  полнотекстовый поиск (Pagefind, поддержка русского), тёмная тема, адаптив,
  русский интерфейс. Страницы — обычный Markdown.
- **Деплой**: GitHub Actions (`withastro/action@v6` + `actions/deploy-pages@v5`)
  на каждый push в `master`.
- Сгенерированного в репозитории нет: страница плана собирается при билде.

## 3. Структура

```
site/
  astro.config.mjs          # site, base: '/ipoteka-regress-kit', defaultLocale: 'ru'
  package.json              # dev/build/preview; prebuild → node scripts/sync-plan.mjs
  scripts/sync-plan.mjs     # docs/plan.md → src/content/docs/plan.mdx (+frontmatter)
  src/content/docs/index.md # лендинг
  src/content/docs/plan.mdx # генерируется при билде (в .gitignore)
.github/workflows/deploy.yml
```

## 4. Страницы

1. **index** — что это и для кого, ключевые возможности списком, блок скачивания,
   CTA «Читать план».
2. **plan** — полный текст `docs/plan.md` (оглавление строится по заголовкам,
   ищется Pagefind-поиском).

**Блок скачивания (на index):** прямые raw-ссылки master-ветки на
`scripts/pretenziya.py`, `scripts/isk.py`, `scripts/cbr_rate.py`,
`requirements.txt` + curl-однострочник для копирования. Raw-ссылки всегда отдают
актуальную версию файлов из ветки — сайт не хранит копий скриптов.

## 5. Синхронизация плана

`sync-plan.mjs` читает `../../docs/plan.md`, добавляет frontmatter
(`title: План стратегии`, `description`, `template: doc`) и пишет
`src/content/docs/plan.mdx`. Запускается автоматически как `prebuild`
(CI и локальный `npm run dev`). Правки плана живут только в `docs/plan.md`.

## 6. Деплой

`deploy.yml`: триггеры — push в `master` + ручной запуск; permissions
`contents: read`, `pages: write`, `id-token: write`; job `build`
(`withastro/action@v6`, node 24) → job `deploy` (`actions/deploy-pages@v5`).

Разовое ручное действие в GitHub: Settings → Pages → Source: **GitHub Actions**.

## 7. .gitignore (дополнение)

```
site/node_modules/
site/dist/
site/.astro/
site/src/content/docs/plan.mdx
```

## 8. Проверки

- Локально: `npm install && npm run build` в `site/` — сборка без ошибок,
  на странице плана присутствует текст из `docs/plan.md`.
- После пуша: workflow зелёный, сайт открывается, raw-ссылки скачивания актуальны.

## 9. Заметки

- Raw-ссылки привязаны к ветке `master` — при переименовании ветки править index.
- Pagefind индексирует русский из коробки (unicode-токенайзер).
- Starlight пока 0.x: обновлять точечно, ломающих изменений в минорных не было.
