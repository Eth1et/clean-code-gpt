import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { Router } from '@angular/router';
import { AuthService } from './shared/services/auth.service';
import { User } from './shared/models/User';
import { Subscription } from 'rxjs';
import { UserService } from './shared/services/user.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy{
  loggedInUser?: User | null;
  userLoggedInSubscription?: Subscription;

  constructor(private router: Router,
              private authService: AuthService,
              private userService: UserService,
              private snackBar: MatSnackBar) {}

  onToggleSidenav(sidenav: MatSidenav): void {
    sidenav.toggle();
  }

  onClose(event: boolean, sidenav: MatSidenav): void {
    if (event) {
      sidenav.close();
    }
  }

  openSnackBar(message: string, action: string): void {
    this.snackBar.open(message, action, { duration: 3000 });
  }

  logout(): void {
    this.authService.logout()
      .then(() => {
        console.log("Logged out successfully!");
        localStorage.setItem('user', JSON.stringify(null));
        this.loggedInUser = null;
        this.openSnackBar('Logged out successfully!', 'close');
      })
      .catch(err => {
        console.error(err);
      })
      .finally(() => {});
  }

  ngOnInit(): void {
    this.userLoggedInSubscription =  this.authService.isUserLoggedIn()
      .subscribe({
        next: user => {
          this.getUserData(user?.uid);
        },
        error: error => {
          console.error(error);
          this.handleUserNotFound();
        }
      });
  }

  private getUserData(uid: string | undefined): void {
    if (uid) {
      this.userLoggedInSubscription = this.userService.readById(uid)
        .subscribe({
          next: snapshot => {
            this.handleUserDataSnapshot(snapshot);
          },
          error: error => {
            console.error(error);
            this.handleUserNotFound();
          }
        });
    }
  }

  private handleUserDataSnapshot(snapshot: any): void {
    if (snapshot.data()) {
      this.loggedInUser = snapshot.data();
      localStorage.setItem('user', JSON.stringify(snapshot.data()));
    } else {
      this.handleUserNotFound();
    }
  }

  private handleUserNotFound(): void {
    localStorage.setItem('user', JSON.stringify(null));
  }

  ngOnDestroy() {
    this.userLoggedInSubscription?.unsubscribe();
  }
}