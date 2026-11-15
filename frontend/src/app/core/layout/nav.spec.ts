import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter, Router } from '@angular/router';
import { NavItem } from '../navigation/nav-items';
import { Nav } from './nav';
import { stubIcons } from '../../../testing/icons';

@Component({ template: '' })
class Dummy {}

const items: NavItem[] = [
  { path: '/', label: 'First', icon: 'one' },
  { path: '/second', label: 'Second', icon: 'two' },
];

async function renderNavAt(url: string): Promise<HTMLElement> {
  TestBed.configureTestingModule({
    providers: [
      provideRouter([
        { path: '', component: Dummy },
        { path: 'second', component: Dummy },
      ]),
      provideHttpClient(),
      provideHttpClientTesting(),
    ],
  });
  stubIcons();
  await TestBed.inject(Router).navigateByUrl(url);

  const fixture = TestBed.createComponent(Nav);
  fixture.componentRef.setInput('items', items);
  await fixture.whenStable();
  return fixture.nativeElement;
}

function linkByLabel(nav: HTMLElement, label: string): HTMLAnchorElement {
  const link = [...nav.querySelectorAll('a')].find((a) => a.textContent?.trim() === label);
  if (!link) throw new Error(`No link with label "${label}"`);
  return link;
}

describe('Nav', () => {
  it('renders a link for each item', async () => {
    const nav = await renderNavAt('/');
    const links = [...nav.querySelectorAll('a')];

    expect(links.map((a) => a.textContent?.trim())).toEqual(['First', 'Second']);
    expect(links.map((a) => a.getAttribute('href'))).toEqual(['/', '/second']);
  });

  it('marks only the current page as current', async () => {
    const nav = await renderNavAt('/second');

    expect(linkByLabel(nav, 'Second').getAttribute('aria-current')).toBe('page');
    expect(linkByLabel(nav, 'First').hasAttribute('aria-current')).toBe(false);
  });

  it('shows the filled icon only for the current page', async () => {
    const nav = await renderNavAt('/second');
    const iconOf = (label: string) =>
      linkByLabel(nav, label).querySelector('mat-icon')?.getAttribute('data-mat-icon-name');

    expect(iconOf('Second')).toBe('two-fill');
    expect(iconOf('First')).toBe('one');
  });
});
