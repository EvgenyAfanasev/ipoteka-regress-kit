import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://evgenyafanasev.github.io',
  base: '/ipoteka-regress-kit',
  integrations: [
    starlight({
      title: 'ipoteka-regress-kit',
      description:
        'Взыскание 1/2 ипотечных платежей с бывшего супруга в порядке регресса: стратегия и генераторы документов',
      defaultLocale: 'ru',
      sidebar: [
        { label: 'Главная', link: '/' },
        { label: 'План стратегии', link: '/plan/' },
      ],
    }),
  ],
});
