import { Route } from '@angular/router';

export interface RouteNavData {
  icon: string;
  label?: string;
}

export interface NavItem {
  path: string;
  label: string;
  icon: string;
}

// Derives main navigation from route config automatically
export function navItemsFromRoutes(routes: readonly Route[] = []): NavItem[] {
  return routes.flatMap((route) => {
    const nav = route.data?.['nav'] as RouteNavData | undefined;
    if (!nav) {
      return [];
    }
    const label = nav.label ?? (typeof route.title === 'string' ? route.title : '');
    return [{ path: `/${route.path ?? ''}`, label, icon: nav.icon }];
  });
}
