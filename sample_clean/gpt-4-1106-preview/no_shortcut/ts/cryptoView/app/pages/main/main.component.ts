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

  private loadCurrentUser() {
    const userJson = localStorage.getItem('user');
    if (userJson) {
      this.currentUser = JSON.parse(userJson) as User;
    }
    console.log('Current User:', this.currentUser);
  }
}