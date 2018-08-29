import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';

import { User } from '../services';

@Injectable()
export class LoggedIn implements CanActivate {
  canActivate(): boolean {
    const user: User = User.getUser();
    return (user !== null);
  }
}
