import { Injectable } from '@angular/core';
import { AngularFirestore, CollectionReference } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable } from 'rxjs';
import { Comment } from '../models/Comment';
import { QueryFn } from '@angular/fire/compat/firestore/interfaces';

@Injectable({
  providedIn: 'root'
})
export class ForumService {
  
  private readonly forumCollectionName: string = 'Forums';
  private readonly commentCollectionName: string = 'Comments';

  constructor(private afs: AngularFirestore) { }

  getForums(): Observable<Forum[]> {
    return this.afs.collection<Forum>(this.forumCollectionName).valueChanges();
  }

  getCommentsByForumId(forumId: number): Observable<Comment[]> {
    return this.afs.collection<Comment>(this.commentCollectionName, ref => this.queryCommentsByForumId(ref, forumId)).valueChanges();
  }

  private queryCommentsByForumId(ref: CollectionReference, forumId: number): QueryFn {
    return ref.where('forumId','==', forumId).orderBy('date', 'asc').limit(25);
  }

  addComment(comment: Comment): Promise<void> {
    return this.afs.collection<Comment>(this.commentCollectionName).add(comment);
  }

  deleteComment(comment: Comment): void {
    this.afs.collection<Comment>(this.commentCollectionName, ref => this.queryCommentToDelete(ref, comment)).get().pipe(
      map(snapshot => {
        snapshot.forEach(doc => {
          doc.ref.delete();
        });
      })
    ).subscribe();
  }

  private queryCommentToDelete(ref: CollectionReference, comment: Comment): QueryFn {
    return ref.where('forumId','==', comment.forumId).where('date','==', comment.date).limit(1);
  }

  updateComment(oldComment: Comment, newComment: Comment): void {
    this.afs.collection<Comment>(this.commentCollectionName, ref => this.queryCommentToUpdate(ref, oldComment)).get().pipe(
      map(snapshot => {
        snapshot.forEach(doc => {
          doc.ref.set(newComment);
        });
      })
    ).subscribe();
  }

  private queryCommentToUpdate(ref: CollectionReference, oldComment: Comment): QueryFn {
    return ref.where('forumId','==', oldComment.forumId).where('date','==', oldComment.date).limit(1);
  }
}