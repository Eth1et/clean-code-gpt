import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/shared/models/User';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  currentUser: User | undefined;

  constructor() {}

  ngOnInit(): void {
    this.setCurrentUserFromLocalStorage();
  }

  private setCurrentUserFromLocalStorage(): void {
    const userString = localStorage.getItem('user');
    if (userString) {
      this.currentUser = JSON.parse(userString);
    }
  }
}