import { Component, Input, Output, EventEmitter, OnInit, OnDestroy, OnChanges } from '@angular/core';
import { Subscription } from 'rxjs';
import { FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Timestamp } from 'firebase/firestore';
import { ForumService } from 'src/app/shared/services/forum.service';
import { Comment } from 'src/app/shared/models/Comment';
import { User } from 'src/app/shared/models/User';
import { Forum } from 'src/app/shared/models/Forum';

@Component({
  selector: 'app-forum-thread',
  templateUrl: './forum-thread.component.html',
  styleUrls: ['./forum-thread.component.scss']
})
export class ForumThreadComponent implements OnInit, OnDestroy, OnChanges {
  @Input() forum?: Forum;
  @Output() forumEmitter: EventEmitter<Forum | undefined> = new EventEmitter<Forum | undefined>();

  currentUser?: User;

  comments: Comment[] = [];
  commentSubscription?: Subscription;
  deleteSubscription?: Subscription;
  editSubscription?: Subscription;

  editedComment?: Comment;

  comment = new FormControl('', [Validators.required]);

  constructor(private forumService: ForumService, private snackBar: MatSnackBar) {}

  ngOnInit(): void {
    this.currentUser = JSON.parse(localStorage.getItem('user') || '{}') as User;

    this.commentSubscription = this.forumService.readAllCommentsByForum(this.forum?.id || 0).subscribe({
      next: (comments: Comment[]) => {
        this.comments = comments;
      },
      error: error => {
        console.error(error);
      }
    });
  }

  openSnackBar(message: string, action: string): void {
    this.snackBar.open(message, action, { duration: 3000 });
  }

  lastComment(comment: Comment): boolean {
    return !!this.comments.length && this.comments[this.comments.length - 1] === comment;
  }

  deleteComment(comment: Comment): void {
    this.deleteSubscription = this.forumService.delete(comment).subscribe({
      next: _ => {
        this.openSnackBar('Comment deleted successfully!', 'close');
      },
      error: err => {
        console.error(err);
        this.openSnackBar(err, 'close');
      }
    });
  }

  editComment(comment: Comment): void {
    if (this.editedComment) {
      this.editedComment = undefined;
      this.comment.setValue('');
      this.openSnackBar('Stopped editing.', 'close');
    } else {
      this.editedComment = comment;
      this.comment.setValue(comment.message);
      this.openSnackBar('Started editing.', 'close');
    }
  }

  addComment(input: HTMLTextAreaElement): void {
    if (!this.comment.valid) {
      this.openSnackBar('Comment must contain at least 1 character!', 'close');
      return;
    }

    const editedSuffix = this.editedComment ? '   <edited>' : '';

    const newComment: Comment = {
      forumId: this.forum?.id || 0,
      sender: this.currentUser as User,
      date: Timestamp.fromDate(new Date()),
      message: this.comment.value + editedSuffix
    };

    if (this.editedComment) {
      this.forumService.update(this.editedComment, newComment).subscribe({
        next: _ => {
          this.openSnackBar('Comment edited successfully!', 'close');
          input.value = '';
          this.goToBottom();
          this.editedComment = undefined;
        },
        error: err => {
          console.error(err);
          this.openSnackBar(err, 'close');
        }
      });
    } else {
      this.forumService.add(newComment).then( _ => {
        this.openSnackBar('Comment added successfully!', 'close');
        input.value = '';
        this.goToBottom();
      }).catch( err => {
        console.error(err);
        this.openSnackBar(err, 'close');
      });
    }
  }

  goToBottom(): void {
    const element = document.getElementById('bottom');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
    }
  }

  backToForums(): void {
    this.forum = undefined;
    this.forumEmitter.emit(this.forum);
  }

  ngOnChanges(): void {
    this.forumEmitter.emit(this.forum);
    this.goToBottom();
  }

  ngOnDestroy(): void {
    this.deleteSubscription?.unsubscribe();
    this.commentSubscription?.unsubscribe();
    this.editSubscription?.unsubscribe();
  }
}