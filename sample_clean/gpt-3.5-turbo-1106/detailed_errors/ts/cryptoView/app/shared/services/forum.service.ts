import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Comment } from '../models/Comment';

@Injectable({
  providedIn: 'root'
})
export class ForumService {
  
  private forumCollectionName: string = 'Forums';
  private commentCollectionName: string = 'Comments';

  constructor(private afs: AngularFirestore) { }

  getAllForums(): Observable<Forum[]> {
    return this.afs.collection<Forum>(this.forumCollectionName).valueChanges();
  }

  getAllCommentsByForum(forumId: number): Observable<Comment[]> {
    return this.afs.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',forumId).orderBy('date', 'asc').limit(25)).valueChanges();
  }

  addComment(comment: Comment): Promise<any> {
    return this.afs.collection<Comment>(this.commentCollectionName).add(comment);
  }

  deleteComment(comment: Comment): Observable<void> {
    return this.afs.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',comment.forumId).where('date','==',comment.date).limit(1))
    .get().pipe(
      map(snapshot => {
        snapshot.forEach(doc => {
          doc.ref.delete();
        });
      })
    );
  }

  updateComment(oldComment: Comment, newComment: Comment): Observable<void> {
    return this.afs.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',oldComment.forumId).where('date','==',oldComment.date).limit(1))
    .get().pipe(
      map(snapshot => {
        snapshot.forEach(doc => {
          doc.ref.set(newComment);
        });
      })
    );
  }
}