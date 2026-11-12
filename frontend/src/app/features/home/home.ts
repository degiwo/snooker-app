import { Component, ChangeDetectionStrategy } from '@angular/core';

@Component({
  selector: 'app-home',
  template: `<p>Welcome</p>`,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export default class Home {}
