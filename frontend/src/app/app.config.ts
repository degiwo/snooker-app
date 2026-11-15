import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners,
  inject,
  provideAppInitializer,
} from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideAppTitle } from './core/navigation/title-strategy';
import { provideHttpClient } from '@angular/common/http';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient(),
    provideAppTitle('degiwo Snooker'),
    provideAppInitializer(() => {
      const sanitizer = inject(DomSanitizer);
      // important: never pass user input here
      inject(MatIconRegistry).addSvgIconResolver((name) =>
        sanitizer.bypassSecurityTrustResourceUrl(`icons/${name}.svg`),
      );
    }),
  ],
};
