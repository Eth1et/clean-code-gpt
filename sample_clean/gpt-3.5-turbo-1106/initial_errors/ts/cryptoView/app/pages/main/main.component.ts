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
    const userFromLocalStorage = localStorage.getItem('user');
    if (userFromLocalStorage) {
      this.currentUser = JSON.parse(userFromLocalStorage);
    }
    console.log(this.currentUser, !this.currentUser);
  }
}