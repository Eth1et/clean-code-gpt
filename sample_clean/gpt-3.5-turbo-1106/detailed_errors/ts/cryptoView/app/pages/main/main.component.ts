import { Component, OnInit } from '@angular/core';
import { User } from 'firebase/auth';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {
  currentUser: User | null = null;

  ngOnInit(): void {
    this.fetchUserFromLocalStorage();
  }

  private fetchUserFromLocalStorage(): void {
    const userFromStorage = localStorage.getItem('user');
    if (userFromStorage) {
      this.currentUser = JSON.parse(userFromStorage) as User;
      console.log(this.currentUser, !this.currentUser);
    }
  }
}