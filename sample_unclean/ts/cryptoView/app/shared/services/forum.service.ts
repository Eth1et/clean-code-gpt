import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { Forum } from '../models/Forum';
import { Observable, map } from 'rxjs';
import { Comment } from '../models/Comment';

@Injectable({
  providedIn: 'root'
})
export class ForumService {
  
  fourmCollectionName: string = 'Forums';
  commentCollectionName: string = 'Comments';


  constructor(private afs: AngularFirestore) { }

  readAll(){
    return this.afs.collection<Forum>(this.fourmCollectionName).valueChanges();
  }

  readAllCommentsByForum(forumId: number): Observable<Array<Comment>>{
    return this.afs.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',forumId).orderBy('date', 'asc').limit(25)).valueChanges();
  }

  add(comment: Comment): Promise<any>{
    return this.afs.collection<Comment>(this.commentCollectionName).add(comment);
  }

  delete(comment: Comment){
    return this.afs.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',comment.forumId).where('date','==',comment.date).limit(1))
    .get().pipe(
      map(snapshot => {
        snapshot.forEach(doc => {
          doc.ref.delete();
        });
      })
    );
  }

  update(oldComment: Comment, newComment: Comment){
    return this.afs.collection<Comment>(this.commentCollectionName, ref => ref.where('forumId','==',oldComment.forumId).where('date','==',oldComment.date).limit(1))
    .get().pipe(
      map(snapshot => {
        snapshot.forEach(doc => {
          doc.ref.set(newComment)
        });
      })
    );
  }
}
