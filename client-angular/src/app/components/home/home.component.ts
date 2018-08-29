import { Component } from '@angular/core';

import { AuthService, User } from '../../services';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html'
})
export class HomeComponent {
  constructor(private authService: AuthService) {}

  getUser(): User {
    return User.getUser();
  }

  logOut(): void {
    this.authService.logOut().subscribe(() => {}, (error) => {
      console.error(error);
    });
  }
}
