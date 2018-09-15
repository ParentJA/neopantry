import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';

import { AuthService, User } from '../../services';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html'
})
export class ProfileComponent {
  profileForm: FormGroup;

  constructor(private authService: AuthService) {
    const user = User.getUser();
    this.profileForm = new FormGroup({
      username: new FormControl(user.username, Validators.required),
      first_name: new FormControl(user.first_name, Validators.required),
      last_name: new FormControl(user.last_name, Validators.required),
      photo: new FormControl('', Validators.required)
    });
  }

  onChange(event): void {
    if (event.target.files && event.target.files.length > 0) {
      this.profileForm.get('photo').setValue(event.target.files[0]);
    }
  }

  onSave(): void {
    this.authService.updateProfile(
      this.profileForm.get('username').value,
      this.profileForm.get('first_name').value,
      this.profileForm.get('last_name').value,
      this.profileForm.get('photo').value
    ).subscribe(() => {}, (error) => {
      console.error(error);
    });
  }
}
