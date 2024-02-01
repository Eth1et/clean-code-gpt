import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable } from 'rxjs';
import { Comment } from '../models/Comment';
import { map, take } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class ForumService {
  
  forumsCollection: string = 'Forums';
  commentsCollection: string = 'Comments';

  constructor(private firestore: AngularFirestore) { }

  getAllForums(): Observable<Forum[]>{
    return this.firestore.collection<Forum>(this.forumsCollection).valueChanges();
  }

  getAllCommentsByForum(forumId: number): Observable<Comment[]>{
    return this.firestore.collection<Comment>(this.commentsCollection, ref => ref.where('forumId','==',forumId).orderBy('date', 'asc').limit(25)).valueChanges();
  }

  addComment(comment: Comment): Promise<any>{
    return this.firestore.collection<Comment>(this.commentsCollection).add(comment);
  }

  deleteComment(comment: Comment): Promise<void>{
    return this.firestore.collection<Comment>(this.commentsCollection, ref => ref.where('forumId','==',comment.forumId).where('date','==',comment.date).limit(1))
    .get().pipe(
      take(1),
      map(snapshot => {
        snapshot.forEach(doc => {
          doc.ref.delete();
        });
      })
    ).toPromise();
  }

  updateComment(oldComment: Comment, newComment: Comment): Promise<void> {
    return this.firestore.collection<Comment>(this.commentsCollection, ref => ref.where('forumId','==',oldComment.forumId).where('date','==',oldComment.date).limit(1))
    .get().pipe(
      take(1),
      map(snapshot => {
        snapshot.forEach(doc => {
          doc.ref.set(newComment);
        });
      })
    ).toPromise();
  }
}