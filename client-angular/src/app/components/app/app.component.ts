import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService, User } from '../../services';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {
  title = 'app';

  get user(): User {
    return User.getUser();
  }

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  logOut(): void {
    this.authService.logOut().subscribe(() => {
      this.router.navigateByUrl('');
    }, (error) => {
      console.error(error);
    });
  }
}
