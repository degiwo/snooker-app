import { Routes } from '@angular/router';
import { Shell } from './core/layout/shell';

export const routes: Routes = [
  {
    path: '',
    component: Shell,
    children: [
      {
        path: '',
        title: 'Home',
        loadComponent: () => import('./features/home/home'),
      },
      {
        path: 'settings',
        title: 'Settings',
        loadComponent: () => import('./features/settings/settings'),
      },
    ],
  },
  { path: '**', redirectTo: '' },
];
