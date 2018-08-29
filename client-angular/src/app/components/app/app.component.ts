import { Component } from '@angular/core';

import { User } from '../../services';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent {
  title = 'app';

  get user(): User {
    return User.getUser();
  }
}
