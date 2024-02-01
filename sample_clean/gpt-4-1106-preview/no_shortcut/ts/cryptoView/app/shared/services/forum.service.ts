import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable } from 'rxjs';
import { Comment } from '../models/Comment';

@Injectable({
  providedIn: 'root'
})
export class ForumService {
  private forumCollectionName: string = 'Forums';
  private commentCollectionName: string = 'Comments';

  constructor(private firestore: AngularFirestore) { }

  getAllForums(): Observable<Forum[]> {
    return this.firestore.collection<Forum>(this.forumCollectionName).valueChanges();
  }

  getCommentsByForumId(forumId: number): Observable<Comment[]> {
    return this.firestore.collection<Comment>(this.commentCollectionName, ref => 
      ref.where('forumId', '==', forumId)
        .orderBy('date', 'asc')
        .limit(25)
    ).valueChanges();
  }

  createComment(comment: Comment): Promise<void> {
    return this.firestore.collection<Comment>(this.commentCollectionName).doc().set(comment);
  }

  removeComment(comment: Comment): Observable<void[]> {
    return this.firestore.collection<Comment>(this.commentCollectionName, ref => 
      ref.where('forumId', '==', comment.forumId).where('date', '==', comment.date).limit(1))
      .snapshotChanges().pipe(
        map(changes => 
          changes.map(change => 
            change.payload.doc.ref.delete()
          )
        )
      );
  }

  updateComment(originalComment: Comment, updatedComment: Comment): Observable<void[]> {
    return this.firestore.collection<Comment>(this.commentCollectionName, ref => 
      ref.where('forumId', '==', originalComment.forumId).where('date', '==', originalComment.date).limit(1))
      .snapshotChanges().pipe(
        map(changes => 
          changes.map(change => 
            change.payload.doc.ref.update(updatedComment)
          )
        )
      );
  }
}