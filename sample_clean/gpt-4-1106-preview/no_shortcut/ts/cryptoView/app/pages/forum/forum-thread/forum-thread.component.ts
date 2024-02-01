import { Component, Input, OnDestroy, OnInit, Output, EventEmitter, OnChanges } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Subscription } from 'rxjs';
import { Timestamp } from 'firebase/firestore';

import { Comment } from 'src/app/shared/models/Comment';
import { User } from 'src/app/shared/models/User';
import { Forum } from 'src/app/shared/models/Forum';
import { ForumService } from 'src/app/shared/services/forum.service';

@Component({
  selector: 'app-forum-thread',
  templateUrl: './forum-thread.component.html',
  styleUrls: ['./forum-thread.component.scss']
})
export class ForumThreadComponent implements OnInit, OnDestroy, OnChanges {
  @Input() forum?: Forum;
  @Output() forumUpdated: EventEmitter<Forum> = new EventEmitter();

  currentUser?: User;
  comments?: Comment[];
  commentControl = new FormControl('', [Validators.required]);
  editedComment?: Comment;

  private commentSubscription: Subscription; 
  private deleteSubscription?: Subscription;
  private editSubscription?: Subscription;

  constructor(private forumService: ForumService, private snackBarService: MatSnackBar) {}

  ngOnInit(): void {
    this.initializeUser();
    this.loadComments();
  }

  initializeUser(): void {
    const userString = localStorage.getItem('user');
    if (userString) {
      this.currentUser = JSON.parse(userString);
    }
  }

  loadComments(): void {
    if (this.forum?.id) {
      this.commentSubscription = this.forumService.readAllCommentsByForum(this.forum.id)
        .subscribe(comments => this.comments = comments);
    }
  }

  displayMessage(message: string, action: string = 'close'): void {
    this.snackBarService.open(message, action, { duration: 3000 });
  }

  isLastComment(comment: Comment): boolean {
    return this.comments?.[this.comments.length - 1] === comment;
  }

  deleteComment(comment: Comment): void {
    this.forumService.delete(comment).subscribe({
      next: () => this.displayMessage('Comment deleted successfully!'),
      error: (error) => this.handleServiceError(error)
    });
  }

  editComment(comment: Comment): void {
    if (this.editedComment) {
      this.cancelEdit();
    } else {
      this.beginEdit(comment);
    }
  }

  beginEdit(comment: Comment): void {
    this.editedComment = comment;
    this.commentControl.setValue(comment.message);
    this.displayMessage('Started editing.');
  }

  cancelEdit(): void {
    this.editedComment = undefined;
    this.commentControl.reset();
    this.displayMessage('Stopped editing.');
  }

  saveComment(input: HTMLTextAreaElement): void {
    if (this.commentControl.invalid) {
      this.displayMessage('Comment must contain at least 1 character!');
      return;
    }

    const newComment = this.createCommentFromInput();

    if (this.editedComment) {
      this.updateComment(newComment, input);
    } else {
      this.addNewComment(newComment, input);
    }
  }

  createCommentFromInput(): Comment {
    return {
      forumId: this.forum?.id,
      sender: this.currentUser,
      date: Timestamp.fromDate(new Date()),
      message: this.commentControl.value + (this.editedComment ? "   <edited>" : "")
    };
  }

  updateComment(comment: Comment, inputElement: HTMLTextAreaElement): void {
    if (this.editedComment) {
      this.forumService.update(this.editedComment, comment).subscribe({
        next: () => {
          this.displayMessage('Comment edited successfully!');
          inputElement.value = "";
          this.scrollToBottom();
          this.editedComment = undefined;
        },
        error: (error) => this.handleServiceError(error)
      });
    }
  }

  addNewComment(comment: Comment, inputElement: HTMLTextAreaElement): void {
    this.forumService.add(comment).then(() => {
      this.displayMessage('Comment added successfully!');
      inputElement.value = "";
      this.scrollToBottom();
    }).catch(this.handleServiceError);
  }

  scrollToBottom(): void {
    const element = document.getElementById('bottom');
    element?.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
  }

  navigateBackToForums(): void {
    this.forum = undefined;
    this.emitForumEvent();
  }

  ngOnChanges(): void {
    this.emitForumEvent();
    this.scrollToBottom();
  }

  ngOnDestroy(): void {
    this.commentSubscription?.unsubscribe();
    this.deleteSubscription?.unsubscribe();
    this.editSubscription?.unsubscribe();
  }

  private handleServiceError(error: any): void {
    console.error(error);
    this.displayMessage('An error occurred. Please try again.');
  }

  private emitForumEvent(): void {
    this.forumUpdated.emit(this.forum);
  }
}