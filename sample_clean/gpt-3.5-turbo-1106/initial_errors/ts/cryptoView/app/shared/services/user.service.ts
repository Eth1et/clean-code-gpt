@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly collectionName = 'Users';

  constructor(private firestore: AngularFirestore) {}

  create(user: User) {
    return this.firestore.collection<User>(this.collectionName).doc(user.id).set(user);
  }

  readById(id: string) {
    return this.firestore.collection<User>(this.collectionName).doc(id).get();
  }

  readByUsername(username: string) {
    return this.firestore.collection<User>(this.collectionName, ref => ref.where('username', '==', username).limit(1)).valueChanges();
  }

  readByEmail(email: string) {
    return this.firestore.collection<User>(this.collectionName, ref => ref.where('email', '==', email).limit(1)).valueChanges();
  }

  readAll() {
    return this.firestore.collection<User>(this.collectionName).valueChanges();
  }

  update(user: User) {
    return this.firestore.collection<User>(this.collectionName).doc(user.id).set(user);
  }

  delete(id: string) {
    return this.firestore.collection<User>(this.collectionName).doc(id).delete();
  }
}