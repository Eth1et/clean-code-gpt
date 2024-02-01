import { Component, OnInit } from '@angular/core';
import { User } from 'firebase/auth';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit{
  currentUser?: User;

  ngOnInit(): void {
    this.loadCurrentUserFromLocalStorage();
  }

  private loadCurrentUserFromLocalStorage(): void {
    const userString = localStorage.getItem('user');
    if (userString) {
      this.currentUser = JSON.parse(userString) as User;
      console.log(this.currentUser, !this.currentUser);
    }
  }
}