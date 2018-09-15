import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { AuthService } from '../../services';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html'
})
export class SignUpComponent {
  signUpForm: FormGroup;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {
    this.signUpForm = new FormGroup({
      username: new FormControl('', Validators.required),
      first_name: new FormControl('', Validators.required),
      last_name: new FormControl('', Validators.required),
      password: new FormControl('', Validators.required),
      photo: new FormControl('', Validators.required)
    });
  }

  onChange(event): void {
    if (event.target.files && event.target.files.length > 0) {
      this.signUpForm.get('photo').setValue(event.target.files[0]);
    }
  }

  onSubmit(): void {
    this.authService.signUp(
      this.signUpForm.get('username').value,
      this.signUpForm.get('first_name').value,
      this.signUpForm.get('last_name').value,
      this.signUpForm.get('password').value,
      this.signUpForm.get('photo').value
    ).subscribe(() => {
      this.router.navigateByUrl('/log-in');
    }, (error) => {
      console.error(error);
    });
  }
}
