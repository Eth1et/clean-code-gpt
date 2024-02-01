import { Injectable } from '@angular/core';
import { User } from '../models/User';
import { AngularFirestore } from '@angular/fire/compat/firestore';

@Injectable({ providedIn: 'root' })
export class UserService {
  collectionName = 'Users';

  constructor(private firestore: AngularFirestore) { }

  createUser(user: User){
    return this.firestore.collection<User>(this.collectionName).doc(user.id).set(user);
  }

  readUserById(id: string){
    return this.firestore.collection<User>(this.collectionName).doc(id).get();
  }

  readUserByUsername(username: string){
    return this.firestore.collection<User>(this.collectionName, ref => ref.where('username', '==', username).limit(1)).valueChanges();
  }

  readUserByEmail(email: string){
    return this.firestore.collection<User>(this.collectionName, ref => ref.where('email', '==', email).limit(1)).valueChanges();
  }

  readAllUsers(){
    return this.firestore.collection<User>(this.collectionName).valueChanges();
  }

  updateUser(user: User){
    return this.firestore.collection<User>(this.collectionName).doc(user.id).update(user);
  }

  deleteUser(id: string){
    return this.firestore.collection<User>(this.collectionName).doc(id).delete();
  }
}