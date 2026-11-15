import { TestBed } from '@angular/core/testing';
import { MatIconRegistry } from '@angular/material/icon';
import { DomSanitizer } from '@angular/platform-browser';

// <mat-icon svgIcon> then can resolve icon names in tests
export function stubIcons(): void {
  const sanitizer = TestBed.inject(DomSanitizer);
  TestBed.inject(MatIconRegistry).addSvgIconResolver((name) =>
    sanitizer.bypassSecurityTrustResourceUrl(`test-icons/${name}.svg`),
  );
}
