import { HttpClient } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ReactiveFormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class App {
  private readonly http = inject(HttpClient);
  private readonly backendUrl = environment.backendUrl;

  form = new FormGroup({
    opponent: new FormControl(''),
    player_score: new FormControl(0),
    opponent_score: new FormControl(0),
  });

  submit() {
    const now = new Date();
    const payload = {
      id: now.getTime(),
      created_at: now.toISOString(),
      date: now.toISOString().split('T')[0],
      opponent_name: this.form.value.opponent ?? '',
      score: this.form.value.player_score ?? 0,
      opponent_score: this.form.value.opponent_score ?? 0,
      high_break: 0,
    };
    this.http.post(`${this.backendUrl}/results`, payload).subscribe({
      next: () => console.log('Result saved'),
      error: (err) => console.error('Failed to save result', err),
    });
  }
}
