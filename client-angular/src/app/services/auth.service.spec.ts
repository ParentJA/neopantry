import { HttpClientTestingModule, HttpTestingController, TestRequest } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { AuthService, User } from './auth.service';

describe('AuthService', () => {
  let authService: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule
      ],
      providers: [ AuthService ]
    });

    authService = TestBed.get(AuthService);
    httpMock = TestBed.get(HttpTestingController);
  });

  it('should allow a user to sign up for a new account', () => {
    let responseData: User = User.create({
      id: 1,
      username: 'test.user@example.com',
      first_name: 'Test',
      last_name: 'User',
      photo: '/media/photos/photo.jpg',
    });
    let photo: File = new File(['photo'], 'photo.jpg', {type: 'image/jpeg'});
    authService.signUp('test.user@example.com', 'Test', 'User', 'pAssw0rd!', photo).subscribe(user => {
      expect(user.id).toBe(responseData.id);
      expect(user.username).toBe(responseData.username);
      expect(user.first_name).toBe(responseData.first_name);
      expect(user.last_name).toBe(responseData.last_name);
      expect(user.photo).toBe(responseData.photo);
    });
    let request: TestRequest = httpMock.expectOne('http://localhost:8000/api/v1/accounts/sign-up/');
    request.flush(responseData);
  });

  it('should allow a user to log in to an existing account', () => {
    let responseData: User = User.create({
      id: 1,
      username: 'test.user@example.com',
      first_name: 'Test',
      last_name: 'User',
      photo: '/media/photos/photo.jpg'
    });
    localStorage.clear();
    authService.logIn('test.user@example.com', 'pAssw0rd!').subscribe(user => {
      expect(user.id).toBe(responseData.id);
      expect(user.username).toBe(responseData.username);
      expect(user.first_name).toBe(responseData.first_name);
      expect(user.last_name).toBe(responseData.last_name);
      expect(user.photo).toBe(responseData.photo);
    });
    let request: TestRequest = httpMock.expectOne('http://localhost:8000/api/v1/accounts/log-in/');
    request.flush(responseData);
    expect(localStorage.getItem('neopantry.user')).toBe(JSON.stringify(responseData));
  });

  it('should allow a user to log out', () => {
    let responseData = {};
    localStorage.setItem('neopantry.user', JSON.stringify({}));
    authService.logOut().subscribe(user => {
      expect(user).toEqual(responseData);
    });
    let request: TestRequest = httpMock.expectOne('http://localhost:8000/api/v1/accounts/log-out/');
    request.flush(responseData);
    expect(localStorage.getItem('nepantry.user')).toBeNull();
  });

  afterEach(() => {
    httpMock.verify();
  });
});
