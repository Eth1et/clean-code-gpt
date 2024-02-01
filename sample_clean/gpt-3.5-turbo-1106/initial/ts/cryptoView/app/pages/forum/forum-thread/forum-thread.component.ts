import { Component, Input, OnDestroy, OnInit, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
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
export class ForumThreadComponent implements OnInit, OnDestroy, OnChanges {
  @Input() forum?: Forum;
  @Output() forumEmitter: EventEmitter<Forum> = new EventEmitter();

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

    this.commentSubscription = this.forumService.readAllCommentsByForum(this.forum?.id as number).subscribe({
      next: (comments: Comment[]) => {
        this.comments = comments;
      },
      error: (error: any) => {
        console.error(error);
      }
    });
  }

  openSnackBar(message: string, action: string): void {
    this.snackBar.open(message, action, { duration: 3000 });
  }

  lastComment(comment: Comment): boolean {
    return this.comments.length > 0 && this.comments[this.comments.length - 1].id === comment.id;
  }

  deleteComment(comment: Comment): void {
    this.deleteSubscription = this.forumService.delete(comment).subscribe({
      next: () => {
        this.openSnackBar('Comment deleted successfully!', 'close');
      },
      error: (error: any) => {
        console.error(error);
        this.openSnackBar(error, 'close');
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

    const newMessage = this.editedComment ? this.comment.value + ' <edited>' : this.comment.value;
    const comment: Comment = {
      forumId: this.forum?.id as number,
      sender: this.currentUser as User,
      date: Timestamp.fromDate(new Date()),
      message: newMessage
    };

    if (this.editedComment) {
      this.forumService.update(this.editedComment, comment).subscribe({
        next: () => {
          this.openSnackBar('Comment edited successfully!', 'close');
          input.value = '';
          this.goToBottom();
          this.editedComment = undefined;
        },
        error: (error: any) => {
          console.error(error);
          this.openSnackBar(error, 'close');
        }
      });
    } else {
      this.forumService.add(comment).then(() => {
        this.openSnackBar('Comment added successfully!', 'close');
        input.value = '';
        this.goToBottom();
      }).catch((error: any) => {
        console.error(error);
        this.openSnackBar(error, 'close');
      });
    }
  }

  goToBottom(): void {
    const element = document.getElementById('bottom');
    element?.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
  }

  backToForums(): void {
    this.forum = undefined;
    this.forumEmitter.emit(this.forum);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes.forum) {
      this.forumEmitter.emit(this.forum);
      this.goToBottom();
    }
  }

  ngOnDestroy(): void {
    this.deleteSubscription?.unsubscribe();
    this.commentSubscription?.unsubscribe();
    this.editSubscription?.unsubscribe();
  }
}