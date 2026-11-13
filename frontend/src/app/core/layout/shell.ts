import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { AppTitleStrategy } from '../navigation/title-strategy';

@Component({
  selector: 'app-shell',
  imports: [RouterOutlet],
  templateUrl: './shell.html',
  styleUrl: './shell.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Shell {
  protected readonly pageTitle = inject(AppTitleStrategy).pageTitle;
}
