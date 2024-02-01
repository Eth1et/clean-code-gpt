import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
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
  loggedInUser?: User;
  private authSubscription?: Subscription;
  private userFetchSubscription?: Subscription;

  constructor(
    private authService: AuthService, 
    private userService: UserService, 
    private snackBar: MatSnackBar
  ) {}

  toggleSidenav(sidenav: MatSidenav): void {
    sidenav.toggle();
  }

  closeSidenavIfTrue(close: boolean, sidenav: MatSidenav): void {
    if (close) {
      sidenav.close();
    }
  }

  showSnackbar(message: string, action: string = 'Close'): void {
    this.snackBar.open(message, action, { duration: 3000 });
  }

  logout(): void {
    this.authService.logout()
      .then(() => {
        this.showSnackbar('Logged out successfully!');
        this.updateUserState(null);
      })
      .catch(error => console.error(error));
  }

  private updateUserState(user: User | null): void {
    localStorage.setItem('user', JSON.stringify(user));
    this.loggedInUser = user;
  }

  private fetchUserDetails(userId: string): void {
    this.userFetchSubscription = this.userService.readById(userId).subscribe({
      next: snapshot => {
        const userDetails = snapshot.data();
        this.updateUserState(userDetails);
      },
      error: error => {
        console.error(error);
        this.updateUserState(null);
      }
    });
  }

  ngOnInit(): void {
    this.authSubscription = this.authService.isUserLoggedIn().subscribe({
      next: user => {
        this.updateUserState(user);
        if (user) {
          this.fetchUserDetails(user.uid);
        }
      },
      error: error => {
        console.error(error);
        this.updateUserState(null);
      }
    });
  }

  ngOnDestroy(): void {
    this.authSubscription?.unsubscribe();
    this.userFetchSubscription?.unsubscribe();
  }
}