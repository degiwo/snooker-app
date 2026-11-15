import { Component, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-settings',
  template: `<p>Settings</p>`,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export default class Settings {}
