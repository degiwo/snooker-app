import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter, TitleStrategy } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { APP_NAME, AppTitleStrategy } from '../navigation/title-strategy';
import { stubIcons } from '../../../testing/icons';
import { Shell } from './shell';

@Component({ template: '' })
class Dummy {}

describe('Shell', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideRouter([
          {
            path: '',
            component: Shell,
            children: [
              { path: '', title: 'First', component: Dummy, data: { nav: { icon: 'one' } } },
              { path: 'hidden', title: 'Hidden', component: Dummy },
            ],
          },
        ]),
        { provide: APP_NAME, useValue: 'App' },
        { provide: TitleStrategy, useExisting: AppTitleStrategy },
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    });
    stubIcons();
  });

  it('shows the title of the current page as heading', async () => {
    const harness = await RouterTestingHarness.create('/hidden');

    expect(harness.routeNativeElement?.querySelector('h1')?.textContent?.trim()).toBe('Hidden');
  });

  it('lists only child pages with nav data in the navigation', async () => {
    const harness = RouterTestingHarness.create('/');
    const labels = [...(await harness).routeNativeElement!.querySelectorAll('nav a')].map((a) =>
      a.textContent?.trim(),
    );

    expect(labels).toEqual(['First']);
  });

  it('moves focus to the main content when the skip link is used', async () => {
    const harness = await RouterTestingHarness.create('/');
    const shell = harness.routeNativeElement!;

    shell.querySelector('button')!.click();

    expect(document.activeElement).toBe(shell.querySelector('main'));
  });
});
