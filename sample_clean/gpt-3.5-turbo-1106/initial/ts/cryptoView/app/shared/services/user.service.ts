import { Injectable } from '@angular/core';
import { User } from '../models/User';
import { AngularFirestore, AngularFirestoreCollection, QueryFn } from '@angular/fire/compat/firestore';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private collectionName = 'Users';
  private userCollection: AngularFirestoreCollection<User>;

  constructor(private afs: AngularFirestore) {
    this.userCollection = this.afs.collection<User>(this.collectionName);
  }

  create(user: User): Promise<void> {
    return this.userCollection.doc(user.id).set(user);
  }

  readById(id: string): Observable<any> {
    return this.userCollection.doc(id).get();
  }

  readByUsername(username: string): Observable<User[]> {
    return this.userCollection
      .ref
      .where('username', '==', username)
      .limit(1)
      .get()
      .then(querySnapshot => {
        const data = [];
        querySnapshot.forEach(doc => {
          data.push(doc.data());
        });
        return data;
      });
  }

  readByEmail(email: string): Observable<User[]> {
    return this.userCollection
      .ref
      .where('email', '==', email)
      .limit(1)
      .get()
      .then(querySnapshot => {
        const data = [];
        querySnapshot.forEach(doc => {
          data.push(doc.data());
        });
        return data;
      });
  }

  readAll(): Observable<User[]> {
    return this.userCollection.valueChanges();
  }

  update(user: User): Promise<void> {
    return this.userCollection.doc(user.id).update(user);
  }

  delete(id: string): Promise<void> {
    return this.userCollection.doc(id).delete();
  }
}
