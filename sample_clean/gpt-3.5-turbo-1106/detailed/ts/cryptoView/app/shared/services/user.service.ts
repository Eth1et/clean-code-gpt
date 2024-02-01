import { Injectable } from '@angular/core';
import { User } from '../models/User';
import { AngularFirestore, AngularFirestoreCollection, QueryFn } from '@angular/fire/compat/firestore';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private readonly collectionName = 'Users';
  private usersCollection: AngularFirestoreCollection<User>;

  constructor(private afs: AngularFirestore) {
    this.usersCollection = afs.collection<User>(this.collectionName);
  }

  create(user: User): Promise<void> {
    return this.usersCollection.doc(user.id).set(user);
  }

  readById(id: string): Observable<any> {
    return this.usersCollection.doc(id).valueChanges();
  }

  private getFilteredUsersCollection(queryFn: QueryFn): Observable<User[]> {
    return this.afs.collection<User>(this.collectionName, queryFn).valueChanges();
  }

  readByUsername(username: string): Observable<User[]> {
    return this.getFilteredUsersCollection(ref => ref.where('username', '==', username).limit(1));
  }

  readByEmail(email: string): Observable<User[]> {
    return this.getFilteredUsersCollection(ref => ref.where('email', '==', email).limit(1));
  }

  readAll(): Observable<User[]> {
    return this.usersCollection.valueChanges();
  }

  update(user: User): Promise<void> {
    return this.usersCollection.doc(user.id).set(user);
  }

  delete(id: string): Promise<void> {
    return this.usersCollection.doc(id).delete();
  }
}