import { Routes } from '@angular/router';

export const routes: Routes = [
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
  { path: '**', redirectTo: '' },
];
