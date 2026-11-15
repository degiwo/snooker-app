import {
  EnvironmentProviders,
  Injectable,
  InjectionToken,
  inject,
  makeEnvironmentProviders,
  signal,
} from '@angular/core';
import { Title } from '@angular/platform-browser';
import { RouterStateSnapshot, TitleStrategy } from '@angular/router';

const APP_NAME = new InjectionToken<string>('APP_NAME');

@Injectable({ providedIn: 'root' })
export class AppTitleStrategy extends TitleStrategy {
  private readonly documentTitle = inject(Title);
  private readonly appName = inject(APP_NAME);

  private readonly _pageTitle = signal('');
  readonly pageTitle = this._pageTitle.asReadonly();

  override updateTitle(snapshot: RouterStateSnapshot): void {
    const page = this.buildTitle(snapshot) ?? '';
    this._pageTitle.set(page);
    this.documentTitle.setTitle(page ? `${page} | ${this.appName}` : this.appName);
  }
}

export function provideAppTitle(appName: string): EnvironmentProviders {
  return makeEnvironmentProviders([
    { provide: APP_NAME, useValue: appName },
    // useExisting instead of useClass: router and Shell must share the same instance
    { provide: TitleStrategy, useExisting: AppTitleStrategy },
  ]);
}
