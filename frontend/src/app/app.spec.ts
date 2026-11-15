import { provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Title } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { appConfig } from './app.config';

describe('App', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [...appConfig.providers, provideHttpClientTesting()],
    });
  });

  it('redirects unknown URLs to the start page', async () => {
    await RouterTestingHarness.create('/does-not-exist');

    expect(TestBed.inject(Router).url).toBe('/');
  });

  it('shows the page title in both heading and browser tab', async () => {
    const harness = await RouterTestingHarness.create('/');
    const heading = harness.routeNativeElement?.querySelector('h1')?.textContent?.trim();

    expect(heading).toBeTruthy();
    expect(TestBed.inject(Title).getTitle()).toContain(heading);
  });
});
