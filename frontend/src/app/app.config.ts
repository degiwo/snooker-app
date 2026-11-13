import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  inject,
  provideAppInitializer,
} from '@angular/core';
import { provideRouter, TitleStrategy } from '@angular/router';
import { routes } from './app.routes';
import { APP_NAME, AppTitleStrategy } from './core/navigation/title-strategy';
import { provideHttpClient } from '@angular/common/http';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient(),
    { provide: APP_NAME, useValue: 'Snooker' },
    { provide: TitleStrategy, useExisting: AppTitleStrategy },
    provideAppInitializer(() => {
      const sanitizer = inject(DomSanitizer);
      inject(MatIconRegistry).addSvgIconResolver((name) =>
        sanitizer.bypassSecurityTrustResourceUrl(`icons/${name}.svg`),
      );
    }),
  ],
};
