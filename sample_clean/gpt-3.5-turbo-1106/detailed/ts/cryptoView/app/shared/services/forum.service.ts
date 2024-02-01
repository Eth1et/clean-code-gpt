import { Injectable } from '@angular/core';
import { AngularFirestore, QueryFn } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable } from 'rxjs';
import { Comment } from '../models/Comment';

@Injectable({
  providedIn: 'root'
})
export class ForumService {
  
  private readonly forumCollectionName: string = 'Forums';
  private readonly commentCollectionName: string = 'Comments';

  constructor(private readonly afs: AngularFirestore) { }

  getAllForums(): Observable<Forum[]> {
    return this.afs.collection<Forum>(this.forumCollectionName).valueChanges();
  }

  getAllCommentsByForum(forumId: number): Observable<Comment[]> {
    return this.afs.collection<Comment>(
      this.commentCollectionName,
      (ref: QueryFn) => ref.where('forumId', '==', forumId).orderBy('date', 'asc').limit(25)
    ).valueChanges();
  }

  addComment(comment: Comment): Promise<any> {
    return this.afs.collection<Comment>(this.commentCollectionName).add(comment);
  }

  deleteComment(comment: Comment): void {
    this.afs.collection<Comment>(
      this.commentCollectionName,
      (ref: QueryFn) => ref.where('forumId', '==', comment.forumId).where('date', '==', comment.date).limit(1)
    ).get().subscribe(snapshot => {
      snapshot.forEach(doc => {
        doc.ref.delete();
      });
    });
  }

  updateComment(oldComment: Comment, newComment: Comment): void {
    this.afs.collection<Comment>(
      this.commentCollectionName,
      (ref: QueryFn) => ref.where('forumId', '==', oldComment.forumId).where('date', '==', oldComment.date).limit(1)
    ).get().subscribe(snapshot => {
      snapshot.forEach(doc => {
        doc.ref.set(newComment)
      });
    });
  }
}