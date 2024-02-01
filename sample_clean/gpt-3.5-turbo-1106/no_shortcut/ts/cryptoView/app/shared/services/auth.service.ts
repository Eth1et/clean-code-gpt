import { Injectable } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/compat/auth';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(private angularFireAuth: AngularFireAuth) {}

  login(email: string, password: string): Promise<any>{
    return this.angularFireAuth.signInWithEmailAndPassword(email, password);
  }

  signup(email: string, password: string): Promise<any>{
    return this.angularFireAuth.createUserWithEmailAndPassword(email, password);
  }

  logout(): Promise<void> {
    return this.angularFireAuth.signOut();
  }

  isLoggedIn(): any {
    return this.angularFireAuth.user;
  }
}