import { Routes } from '@angular/router';
import { Shell } from './core/layout/shell';
import { RouteNavData } from './core/navigation/nav-items';

export const routes: Routes = [
  {
    path: '',
    component: Shell,
    children: [
      {
        path: '',
        title: 'Home',
        loadComponent: () => import('./features/home/home'),
        data: { nav: { icon: 'home' } satisfies RouteNavData },
      },
      {
        path: 'settings',
        title: 'Settings',
        loadComponent: () => import('./features/settings/settings'),
        data: { nav: { icon: 'settings' } satisfies RouteNavData },
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
