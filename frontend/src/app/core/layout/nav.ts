import { ChangeDetectionStrategy, Component, input } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { NavItem } from '../navigation/nav-items';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-nav',
  imports: [RouterLink, RouterLinkActive, MatIcon],
  templateUrl: './nav.html',
  styleUrl: './nav.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Nav {
  readonly items = input.required<readonly NavItem[]>();
}
