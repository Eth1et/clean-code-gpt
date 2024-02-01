import { Injectable } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private authentication: AngularFireAuth) {}

  login(email: string, password: string): Promise<any>{
    return this.authentication.signInWithEmailAndPassword(email, password);
  }

  signup(email: string, password: string): Promise<any>{
    return this.authentication.createUserWithEmailAndPassword(email, password);
  }

  logout(): Promise<any> {
    return this.authentication.signOut();
  }

  isLoggedIn(): Promise<any>{
    return this.authentication.user;
  }
}