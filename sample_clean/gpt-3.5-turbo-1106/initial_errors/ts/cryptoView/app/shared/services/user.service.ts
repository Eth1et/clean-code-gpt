import { Injectable } from '@angular/core';
import { User } from '../models/User';
import { AngularFirestore, AngularFirestoreCollection, DocumentReference } from '@angular/fire/compat/firestore';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private collectionName = 'Users';
  private usersCollection: AngularFirestoreCollection<User>;

  constructor(private afs: AngularFirestore) {
    this.usersCollection = this.afs.collection<User>(this.collectionName);
  }

  create(user: User): Promise<void> {
    return this.usersCollection.doc(user.id).set({ ...user });
  }

  readById(id: string): Observable<User | undefined> {
    return this.usersCollection.doc(id).valueChanges();
  }

  readByUsername(username: string): Observable<User[]> {
    return this.afs.collection<User>(this.collectionName, ref => ref.where('username', '==', username).limit(1)).valueChanges();
  }

  readByEmail(email: string): Observable<User[]> {
    return this.afs.collection<User>(this.collectionName, ref => ref.where('email', '==', email).limit(1)).valueChanges();
  }

  readAll(): Observable<User[]> {
    return this.usersCollection.valueChanges();
  }

  update(user: User): Promise<void> {
    return this.usersCollection.doc(user.id).update({ ...user });
  }

  delete(id: string): Promise<void> {
    return this.usersCollection.doc(id).delete();
  }
}