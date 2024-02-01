import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { User } from '../models/User';

@Injectable({
  providedIn: 'root'
})
export class AuthRedirectGuard implements CanActivate {
  
  private readonly redirectUrl: string = 'main';
  
  constructor(private router: Router){}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    
    const loggedInUser: User | null = this.getLoggedInUser();

    if (loggedInUser) {
      return this.getRedirectUrl();
    }
    
    return true;
  }

  private getLoggedInUser(): User | null {
    const userJson: string | null = localStorage.getItem('user');
    return userJson ? JSON.parse(userJson) : null;
  }

  private getRedirectUrl(): UrlTree {
    return this.router.parseUrl(this.redirectUrl);
  }
}