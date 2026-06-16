import { provideHttpClient } from '@angular/common/http';
import { Component, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ReactiveFormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
})
export class App {
  protected readonly title = signal('Snooker App');

  backend_url = 'http://localhost:8000';
  client = provideHttpClient();

  form = new FormGroup({
    opponent: new FormControl(''),
    player_score: new FormControl(0),
    opponent_score: new FormControl(0),
  });

  submit() {
    console.log(this.form.value);
  }
}
