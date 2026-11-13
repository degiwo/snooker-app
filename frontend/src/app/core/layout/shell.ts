import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { RouterOutlet, ActivatedRoute } from '@angular/router';
import { AppTitleStrategy } from '../navigation/title-strategy';
import { navItemsFromRoutes } from '../navigation/nav-items';
import { Nav } from './nav';

@Component({
  selector: 'app-shell',
  imports: [RouterOutlet, Nav],
  templateUrl: './shell.html',
  styleUrl: './shell.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Shell {
  protected readonly pageTitle = inject(AppTitleStrategy).pageTitle;
  protected readonly navItems = navItemsFromRoutes(inject(ActivatedRoute).routeConfig?.children);
}
