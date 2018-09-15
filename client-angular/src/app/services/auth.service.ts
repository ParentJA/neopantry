import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';
import { finalize, map, tap } from 'rxjs/operators';

export class User {
  static create(data: any): User {
    return new User(
      data.id,
      data.username,
      data.first_name,
      data.last_name,
      data.photo
    );
  }

  static getUser(): User {
    const userData = localStorage.getItem('neopantry.user');
    if (userData) {
      return User.create(JSON.parse(userData));
    }
    return null;
  }

  constructor(
    public id: number,
    public username: string,
    public first_name: string,
    public last_name: string,
    public photo: any
  ) {}
}

@Injectable()
export class AuthService {
  constructor(private http: HttpClient) {}

  signUp(
    username: string,
    first_name: string,
    last_name: string,
    password: string,
    photo: any
  ): Observable<User> {
    const url = '/api/v1/accounts/sign-up/';
    const formData = new FormData();
    formData.append('username', username);
    formData.append('first_name', first_name);
    formData.append('last_name', last_name);
    formData.append('password1', password);
    formData.append('password2', password);
    formData.append('photo', photo);
    return this.http.request('POST', url, {body: formData}).pipe(
      map((user: any) => {
        return User.create(user);
      })
    );
  }

  logIn(username: string, password: string): Observable<User> {
    const url = '/api/v1/accounts/log-in/';
    return this.http.post(url, {username, password}).pipe(
      map((user: any) => {
        return User.create(user);
      }),
      tap((user: User) => localStorage.setItem('neopantry.user', JSON.stringify(user)))
    );
  }

  logOut(): Observable<any> {
    const url = '/api/v1/accounts/log-out/';
    return this.http.delete(url).pipe(
      finalize(() => localStorage.removeItem('neopantry.user'))
    );
  }

  retrieveProfile(): Observable<User> {
    const url = '/api/v1/accounts/profile/';
    return this.http.get<User>(url).pipe(
      map(user => User.create(user))
    );
  }

  updateProfile(
    username: string,
    first_name: string,
    last_name: string,
    photo: any
  ): Observable<User> {
    const url = '/api/v1/accounts/profile/';
    const formData = new FormData();
    formData.append('username', username);
    formData.append('first_name', first_name);
    formData.append('last_name', last_name);
    formData.append('photo', photo);
    return this.http.request('PATCH', url, {body: formData}).pipe(
      map((user: any) => {
        return User.create(user);
      })
    );
  }
}
