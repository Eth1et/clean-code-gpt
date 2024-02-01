import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Subscription } from 'rxjs';
import { Comment } from 'src/app/shared/models/Comment';
import { Forum } from 'src/app/shared/models/Forum';
import { User } from 'src/app/shared/models/User';
import { ForumService } from 'src/app/shared/services/forum.service';
import { Timestamp } from 'firebase/firestore';

@Component({
  selector: 'app-forum-thread',
  templateUrl: './forum-thread.component.html',
  styleUrls: ['./forum-thread.component.scss']
})
export class ForumThreadComponent implements OnInit, OnDestroy, OnChanges {
  @Input() forum!: Forum;
  @Output() forumEmitter = new EventEmitter<Forum | undefined>();

  currentUser: User | undefined;

  comments: Comment[] | undefined;
  commentSubscription: Subscription | undefined;
  deleteSubscription: Subscription | undefined;
  editSubscription: Subscription | undefined;

  editedComment: Comment | undefined;

  comment = new FormControl('', [Validators.required]);

  constructor(private forumService: ForumService, private snackBar: MatSnackBar) {}

  ngOnInit(): void {
    const user = localStorage.getItem('user');
    if (user) {
      this.currentUser = JSON.parse(user) as User;
    }

    this.commentSubscription = this.forumService.readAllCommentsByForum(this.forum?.id as number).subscribe({
      next: comments => {
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
    return !!this.comments && this.comments[this.comments.length - 1] === comment;
  }

  deleteComment(comment: Comment): void {
    this.deleteSubscription = this.forumService.delete(comment).subscribe({
      next: _ => {
        this.openSnackBar('Comment deleted successfully!', 'close');
      },
      error: error => {
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

    const comment: Comment = {
      forumId: this.forum?.id as number,
      sender: this.currentUser as User,
      date: Timestamp.fromDate(new Date()),
      message: this.comment.value + (this.editedComment ? '   <edited>' : '')
    };

    if (this.editedComment) {
      this.editCommentProcess(input, comment);
    } else {
      this.addCommentProcess(input, comment);
    }
  }

  editCommentProcess(input: HTMLTextAreaElement, comment: Comment): void {
    this.editSubscription = this.forumService.update(this.editedComment, comment).subscribe({
      next: _ => {
        this.openSnackBar('Comment edited successfully!', 'close');
        input.value = '';
        this.goToBottom();
        this.editedComment = undefined;
      },
      error: error => {
        console.error(error);
        this.openSnackBar(error, 'close');
      }
    });
  }

  addCommentProcess(input: HTMLTextAreaElement, comment: Comment): void {
    this.forumService.add(comment).then(_ => {
      this.openSnackBar('Comment added successfully!', 'close');
      input.value = '';
      this.goToBottom();
    }).catch(error => {
      console.error(error);
      this.openSnackBar(error, 'close');
    });
  }

  goToBottom(): void {
    const element = document.getElementById('bottom');
    element?.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
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