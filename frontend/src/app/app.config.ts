import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter, TitleStrategy } from '@angular/router';
import { routes } from './app.routes';
import { APP_NAME, AppTitleStrategy } from './core/navigation/title-strategy';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    { provide: APP_NAME, useValue: 'Snooker' },
    { provide: TitleStrategy, useExisting: AppTitleStrategy },
  ],
};
