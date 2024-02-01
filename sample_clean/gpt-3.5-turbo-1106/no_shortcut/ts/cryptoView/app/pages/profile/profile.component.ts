import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/shared/models/user.model';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  currentUser: User | undefined;

  constructor() {}

  ngOnInit(): void {
    this.loadCurrentUser();
  }

  private loadCurrentUser(): void {
    const userFromLocalStorage = localStorage.getItem('user');
    if (userFromLocalStorage) {
      this.currentUser = JSON.parse(userFromLocalStorage);
    }
  }
}