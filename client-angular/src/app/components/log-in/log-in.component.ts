import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services';

@Component({
  selector: 'app-log-in',
  templateUrl: './log-in.component.html'
})
export class LogInComponent {
  logInForm: FormGroup;
  constructor(
    private router: Router,
    private authService: AuthService
  ) {
    this.logInForm = new FormGroup({
      username: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required)
    });
  }
  onSubmit(): void {
    this.authService.logIn(
      this.logInForm.get('username').value,
      this.logInForm.get('password').value
    ).subscribe(user => {
      this.router.navigateByUrl('');
    }, (error) => {
      console.error(error);
    });
  }
}
