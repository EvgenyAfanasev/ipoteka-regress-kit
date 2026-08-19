// Синхронизация docs/plan.md -> site/src/content/docs/plan.mdx
// Запускается автоматически: перед `astro dev` (скрипт dev) и перед сборкой (prebuild).
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const src = join(siteRoot, '..', 'docs', 'plan.md');
const dst = join(siteRoot, 'src', 'content', 'docs', 'plan.mdx');

const plan = readFileSync(src, 'utf8');
const frontmatter = [
  '---',
  'title: План стратегии',
  'description: Полный план взыскания регрессной доли ипотечных платежей — правовой каркас, этапы, сроки, шаблоны претензии и иска',
  '---',
].join('\n');

mkdirSync(dirname(dst), { recursive: true });
writeFileSync(dst, `${frontmatter}\n\n${plan}\n`, 'utf8');
console.log(`plan.mdx обновлён из docs/plan.md (${plan.split('\n').length} строк)`);
