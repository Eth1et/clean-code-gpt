import { Injectable } from '@angular/core';
import { AngularFirestore, CollectionReference, Query } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable } from 'rxjs';
import { Comment } from '../models/Comment';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ForumService {
  
  private readonly fourmCollectionName = 'Forums';
  private readonly commentCollectionName = 'Comments';

  constructor(private afs: AngularFirestore) { }

  readAll(): Observable<Forum[]> {
    return this.afs.collection<Forum>(this.fourmCollectionName).valueChanges();
  }

  readAllCommentsByForum(forumId: number): Observable<Comment[]> {
    return this.afs.collection<Comment>(this.commentCollectionName, ref => this.getCommentsQuery(ref, forumId)).valueChanges();
  }

  private getCommentsQuery(ref: CollectionReference, forumId: number): Query {
    return ref.where('forumId', '==', forumId).orderBy('date', 'asc').limit(25);
  }

  add(comment: Comment): Promise<any> {
    return this.afs.collection<Comment>(this.commentCollectionName).add(comment);
  }

  delete(comment: Comment): Observable<void> {
      return this.afs.collection<Comment>(this.commentCollectionName, ref => this.getCommentQuery(ref, comment)).get()
      .pipe(
        map(snapshot => {
          snapshot.forEach(doc => doc.ref.delete());
        })
      );
  }

  private getCommentQuery(ref: CollectionReference, comment: Comment): Query {
    return ref.where('forumId', '==', comment.forumId).where('date', '==', comment.date).limit(1);
  }

  update(oldComment: Comment, newComment: Comment): Observable<void> {
    return this.afs.collection<Comment>(this.commentCollectionName, ref => this.getCommentQuery(ref, oldComment)).get()
    .pipe(
      map(snapshot => {
        snapshot.forEach(doc => doc.ref.set(newComment));
      })
    );
  }
}