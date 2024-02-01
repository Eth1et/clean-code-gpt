import { Injectable } from '@angular/core';
import { AngularFirestore, AngularFirestoreCollection, QueryFn } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable } from 'rxjs';
import { Comment } from '../models/Comment';

@Injectable({
  providedIn: 'root'
})
export class ForumService {
  
  private forumCollection: AngularFirestoreCollection<Forum>;
  private commentCollection: AngularFirestoreCollection<Comment>;
  
  constructor(private afs: AngularFirestore) {
    this.forumCollection = afs.collection<Forum>('Forums');
    this.commentCollection = afs.collection<Comment>('Comments');
  }

  readAll(): Observable<Forum[]> {
    return this.forumCollection.valueChanges();
  }

  readAllCommentsByForum(forumId: number): Observable<Comment[]> {
    return this.commentCollection.ref.where('forumId', '==', forumId)
      .orderBy('date', 'asc').limit(25).valueChanges();
  }

  add(comment: Comment): Promise<any> {
    return this.commentCollection.add(comment);
  }

  delete(comment: Comment): Observable<void> {
    return this.commentCollection.ref.where('forumId', '==', comment.forumId)
      .where('date', '==', comment.date).limit(1)
      .get()
      .pipe(
        switchMap(snapshot => {
          return snapshot.docs[0]?.ref.delete() || Promise.resolve();
        })
      );
  }

  update(oldComment: Comment, newComment: Comment): Observable<void> {
    return this.commentCollection.ref.where('forumId', '==', oldComment.forumId)
      .where('date', '==', oldComment.date).limit(1)
      .get()
      .pipe(
        switchMap(snapshot => {
          return snapshot.docs[0]?.ref.set(newComment) || Promise.resolve();
        })
      );
  }
}