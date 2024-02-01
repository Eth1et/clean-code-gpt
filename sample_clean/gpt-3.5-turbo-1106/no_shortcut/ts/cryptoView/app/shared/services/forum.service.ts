import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable, from, map } from 'rxjs';
import { Comment } from '../models/Comment';

@Injectable({
  providedIn: 'root'
})
export class ForumService {
  
  forumCollectionName: string = 'Forums';
  commentCollectionName: string = 'Comments';


  constructor(private firestore: AngularFirestore) { }

  getAllForums(): Observable<Forum[]> {
    return this.firestore.collection<Forum>(this.forumCollectionName).valueChanges();
  }

  getAllCommentsByForum(forumId: number): Observable<Comment[]> {
    return this.firestore.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',forumId).orderBy('date', 'asc').limit(25)).valueChanges();
  }

  addComment(comment: Comment): Promise<any> {
    return this.firestore.collection<Comment>(this.commentCollectionName).add(comment);
  }

  deleteComment(comment: Comment): Observable<any> {
    return from(
      this.firestore.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',comment.forumId).where('date','==',comment.date).limit(1)).get().pipe(
        map(snapshot => {
          snapshot.forEach(doc => {
            doc.ref.delete();
          });
        })
      )
    );
  }

  updateComment(oldComment: Comment, newComment: Comment): Observable<any> {
    return from(
      this.firestore.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',oldComment.forumId).where('date','==',oldComment.date).limit(1)).get().pipe(
        map(snapshot => {
          snapshot.forEach(doc => {
            doc.ref.set(newComment);
          });
        })
      )
    );
  }
}