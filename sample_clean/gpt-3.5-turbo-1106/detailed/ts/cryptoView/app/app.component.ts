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
  loggedInUser: User | null | undefined;
  userLoggedInSubscription: Subscription | undefined;
  getUserSubscription: Subscription | undefined;

  constructor(
    private router: Router,
    private authService: AuthService,
    private userService: UserService,
    private snackBar: MatSnackBar
  ){}

  onToggleSidenav(sidenav: MatSidenav){
    sidenav.toggle();
  }

  onClose(event: any, sidenav: MatSidenav){
    if (event === true){
      sidenav.close();
    }
  }

  openSnackBar(message: string, action: string){
    this.snackBar.open(message, action, {duration: 3000});
  }

  logout(){
    this.authService.logout().then(() =>{
      console.log("Logged out successfully!");
      this.handleLogout();
      this.openSnackBar('Logged out successfully!', 'close');
    }).catch(err => {
      console.error(err);
    });
  }

  private handleLogout(){
    localStorage.setItem('user', JSON.stringify(null));
    this.loggedInUser = null;
  }

  ngOnInit(): void {
    this.subscribeToUserLoggedIn();
  }

  private subscribeToUserLoggedIn(){
    this.userLoggedInSubscription =  this.authService.isUserLoggedIn().subscribe({
      next: user => {
        this.handleUserLoggedIn(user);
      }, 
      error: error =>{
        console.error(error);
        this.handleUserLoggedInFailure();
      }
    });
  }

  private handleUserLoggedIn(user: User | null){
    if(user){
      this.userService.readById(user.uid as string).subscribe({
        next: snapshot => {
          this.handleUserSnapshot(snapshot);
        },
        error: error => {
          console.error(error);
          this.handleUserSnapshotFailure();
        }
      });
    } else {
      this.handleUserSnapshot(null);
    }
  }

  private handleUserSnapshot(snapshot: any){
    if(snapshot && snapshot.data()){
      this.loggedInUser = snapshot.data();
      localStorage.setItem('user', JSON.stringify(snapshot.data()));
    } else {
      this.handleUserSnapshotFailure();
    }
  }

  private handleUserSnapshotFailure(){
    localStorage.setItem('user', JSON.stringify(null));
    this.loggedInUser = null;
  }

  private handleUserLoggedInFailure(){
    localStorage.setItem('user', JSON.stringify(null));
    this.loggedInUser = null;
  }

  ngOnDestroy(){
    this.userLoggedInSubscription?.unsubscribe();
    this.getUserSubscription?.unsubscribe();
  }
}