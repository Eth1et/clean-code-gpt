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
export class AppComponent implements OnInit, OnDestroy {
  loggedInUser: User | null | undefined;
  userLoggedInSubscription: Subscription | undefined;
  getUserSubscription: Subscription | undefined;

  constructor(
    private router: Router,
    private authService: AuthService,
    private userService: UserService,
    private snackBar: MatSnackBar
  ) {}

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

  logout(_?: boolean): void {
    this.authService.logout().then(() => {
      console.log('Logged out successfully!');
      localStorage.setItem('user', JSON.stringify(null));
      this.loggedInUser = null;
      this.openSnackBar('Logged out successfully!', 'close');
    }).catch(err => {
      console.error(err);
    }).finally(() => {
      // Perform any necessary cleanup
    });
  }

  ngOnInit(): void {
    this.userLoggedInSubscription = this.authService.isUserLoggedIn().subscribe({
      next: user => {
        this.updateUserData(user?.uid as string);
      },
      error: error => {
        console.error(error);
        this.updateLoggedInUser(null);
      }
    });
  }

  ngOnDestroy(): void {
    this.userLoggedInSubscription?.unsubscribe();
    this.getUserSubscription?.unsubscribe();
  }

  private updateUserData(uid: string): void {
    this.getUserSubscription = this.userService.readById(uid).subscribe({
      next: snapshot => {
        const userData = snapshot.data();
        if (userData) {
          this.updateLoggedInUser(userData);
        } else {
          this.updateLoggedInUser(null);
        }
      },
      error: error => {
        console.error(error);
        this.updateLoggedInUser(null);
      }
    });
  }

  private updateLoggedInUser(user: User | null): void {
    this.loggedInUser = user;
    localStorage.setItem('user', JSON.stringify(user));
  }
}