import { Route } from '@angular/router';
import { navItemsFromRoutes } from './nav-items';

describe('navItemsForRoutes', () => {
  it('creates an item for each route with nav data', () => {
    const routes: Route[] = [
      { path: '', title: 'First', data: { nav: { icon: 'one' } } },
      { path: 'second', title: 'Second', data: { nav: { icon: 'two' } } },
    ];

    expect(navItemsFromRoutes(routes)).toEqual([
      { path: '/', label: 'First', icon: 'one' },
      { path: '/second', label: 'Second', icon: 'two' },
    ]);
  });

  it('skips routes without nav data', () => {
    const routes: Route[] = [
      { path: 'visible', title: 'Visible', data: { nav: { icon: 'x' } } },
      { path: 'hidden', title: 'Hidden' },
    ];

    expect(navItemsFromRoutes(routes).map((item) => item.path)).toEqual(['/visible']);
  });

  it('prefers an explicit nav label over the route title', () => {
    const routes: Route[] = [
      { path: 'x', title: 'Long Page Title', data: { nav: { icon: 'x', label: 'Short' } } },
    ];

    expect(navItemsFromRoutes(routes)[0].label).toBe('Short');
  });

  it('returns no items when there are no routes', () => {
    expect(navItemsFromRoutes(undefined)).toEqual([]);
  });
});
