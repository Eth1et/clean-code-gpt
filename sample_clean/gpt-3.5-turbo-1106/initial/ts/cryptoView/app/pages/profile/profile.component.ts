import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/shared/models/User';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  currentUser?: User;

  constructor() {}

  ngOnInit(): void {
    this.getCurrentUserFromLocalStorage();
  }

  private getCurrentUserFromLocalStorage(): void {
    const userJson = localStorage.getItem('user');
    if (userJson) {
      this.currentUser = JSON.parse(userJson);
    }
  }
}