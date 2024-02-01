import { Component, OnInit } from '@angular/core';
import { User } from 'firebase/auth';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {
  currentUser?: User;

  ngOnInit(): void {
    this.loadCurrentUser();
  }

  private loadCurrentUser(): void {
    const userFromLocalStorage = localStorage.getItem('user');
    if (userFromLocalStorage) {
      this.currentUser = JSON.parse(userFromLocalStorage) as User;
      console.log('Current user:', this.currentUser);
    } else {
      console.log('No user found in local storage');
    }
  }
}