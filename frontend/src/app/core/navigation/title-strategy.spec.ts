import { Component } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { Title } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { AppTitleStrategy, provideAppTitle } from './title-strategy';

@Component({ template: '' })
class Dummy {}

describe('AppTitleStrategy', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        provideRouter([
          { path: 'with-title', title: 'Page', component: Dummy },
          { path: 'without-title', component: Dummy },
        ]),
        provideAppTitle('App'),
      ],
    });
  });

  it('appends the app name to the page title', async () => {
    await RouterTestingHarness.create('/with-title');

    expect(TestBed.inject(Title).getTitle()).toBe('Page | App');
    expect(TestBed.inject(AppTitleStrategy).pageTitle()).toBe('Page');
  });

  it('shows only the app name when the route has no title', async () => {
    await RouterTestingHarness.create('/without-title');

    expect(TestBed.inject(Title).getTitle()).toBe('App');
    expect(TestBed.inject(AppTitleStrategy).pageTitle()).toBe('');
  });
});
