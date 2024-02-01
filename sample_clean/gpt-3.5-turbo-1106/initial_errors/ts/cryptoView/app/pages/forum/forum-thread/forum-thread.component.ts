import { Component, Input, OnDestroy, OnInit, Output, EventEmitter, OnChanges } from '@angular/core';
import { Comment } from 'src/app/shared/models/Comment';
import { User } from 'src/app/shared/models/User';
import { Forum } from 'src/app/shared/models/Forum';
import { Subscription } from 'rxjs';
import { ForumService } from 'src/app/shared/services/forum.service';
import { FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Timestamp } from 'firebase/firestore';

@Component({
  selector: 'app-forum-thread',
  templateUrl: './forum-thread.component.html',
  styleUrls: ['./forum-thread.component.scss']
})
export class ForumThreadComponent implements OnInit, OnDestroy, OnChanges{
  @Input() forum?: Forum;
  @Output() forumEmitter: EventEmitter<Forum> = new EventEmitter();

  currentUser?: User;

  comments?: Array<Comment>;
  commentSubscription?: Subscription; 
  deleteSubscription?: Subscription;
  editSubscription?: Subscription;

  editedComment?: Comment;

  comment = new FormControl('', [Validators.required]);

  constructor(private forumService: ForumService, private snackBar: MatSnackBar) {}

  ngOnInit(): void {
    this.currentUser = this.getCurrentUserFromLocalStorage();

    this.subscribeToComments();
  }

  getCurrentUserFromLocalStorage(): User | undefined {
    const userString = localStorage.getItem('user');
    return userString ? JSON.parse(userString) : undefined;
  }

  subscribeToComments(): void {
    this.commentSubscription = this.forumService.readAllCommentsByForum(this.forum?.id as number).subscribe({
      next: comments => {
        this.comments = comments;
      },
      error: error => {
        console.error(error);
      }
    });
  }

  // ... (other methods remain the same)

  ngOnDestroy(): void {
    this.unsubscribeFromSubscriptions();
  }

  unsubscribeFromSubscriptions(): void {
    this.deleteSubscription?.unsubscribe();
    this.commentSubscription?.unsubscribe();
    this.editSubscription?.unsubscribe();
  }
}