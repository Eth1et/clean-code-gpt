import { 
  Component, 
  Input, 
  OnDestroy, 
  OnInit, 
  Output, 
  EventEmitter, 
  OnChanges 
} from '@angular/core';
import { 
  Comment 
} from 'src/app/shared/models/Comment';
import { 
  User 
} from 'src/app/shared/models/User';
import { 
  Forum 
} from 'src/app/shared/models/Forum';
import { 
  Subscription 
} from 'rxjs';
import { 
  ForumService 
} from 'src/app/shared/services/forum.service';
import { 
  FormControl, 
  Validators 
} from '@angular/forms';
import { 
  MatSnackBar 
} from '@angular/material/snack-bar';
import { 
  Timestamp 
} from 'firebase/firestore';

@Component({
  selector: 'app-forum-thread',
  templateUrl: './forum-thread.component.html',
  styleUrls: ['./forum-thread.component.scss']
})
export class ForumThreadComponent implements OnInit, OnDestroy, OnChanges {
  @Input() forum?: Forum;
  @Output() forumEmitter: EventEmitter<Forum> = new EventEmitter();

  currentUser?: User;
  comments?: Array<Comment>;
  commentSubscription?: Subscription; 
  deleteSubscription?: Subscription;
  editSubscription?: Subscription;
  editedComment?: Comment;
  comment = new FormControl('', [Validators.required]);

  constructor(
    private forumService: ForumService, 
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.currentUser = JSON.parse(localStorage.getItem('user') as string) as User;
    this.subscribeToComments();
  }

  subscribeToComments() {
    this.commentSubscription = this.forumService
    .readAllCommentsByForum(this.forum?.id as number)
    .subscribe({
      next: (comments) => {
        this.comments = comments;
      },
      error: this.handleCommentSubscriptionError.bind(this)
    });
  }

  handleCommentSubscriptionError(error: any) {
    console.error(error);
  }

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, { duration: 3000 });
  }

  lastComment(comment: Comment): boolean {
    return (
      this.comments && this.comments[this.comments.length - 1] === comment
    ) as boolean;
  }

  deleteComment(comment: Comment) {
    this.deleteSubscription = this.forumService.delete(comment).subscribe({
      next: (_) => {
        this.openSnackBar('Comment deleted successfully!', 'close');
      },
      error: this.handleDeleteCommentError.bind(this)
    });
  }

  handleDeleteCommentError(error: any) {
    console.error(error);
    this.openSnackBar(error, 'close');
  }

  editComment(comment: Comment) {
    if (this.editedComment) {
      this.editedComment = undefined;
      this.comment.setValue('');
      this.openSnackBar('Stopped editing.', 'close');
    } else {
      this.startEditing(comment);
    }
  }

  startEditing(comment: Comment) {
    this.editedComment = comment;
    this.comment.setValue(comment.message);
    this.openSnackBar('Started editing.', 'close');
  }

  addComment(input: HTMLTextAreaElement) {
    if (!this.comment?.valid) {
      this.openSnackBar(
        'Comment must contain at least 1 character!',
        'close'
      );
      return;
    }

    const newComment = this.createComment();

    if (this.editedComment) {
      this.updateComment(input, newComment);
    } else {
      this.saveComment(input, newComment);
    }
  }

  createComment(): Comment {
    return {
      forumId: this.forum?.id as number,
      sender: this.currentUser as User,
      date: Timestamp.fromDate(new Date()),
      message: this.comment?.value + (this.editedComment ? '   <edited>' : '')
    };
  }

  updateComment(input: HTMLTextAreaElement, newComment: Comment) {
    this.editSubscription = this.forumService
      .update(this.editedComment, newComment)
      .subscribe({
        next: (_) => {
          this.handleCommentUpdateSuccess(input);
        },
        error: this.handleEditCommentError.bind(this)
      });
  }

  saveComment(input: HTMLTextAreaElement, newComment: Comment) {
    this.forumService.add(newComment).then(
      (_) => {
        this.handleCommentAddSuccess(input);
      }).catch(this.handleAddCommentError.bind(this));
  }

  handleEditCommentError(error: any) {
    console.error(error);
    this.openSnackBar(error, 'close');
  }

  handleAddCommentError(error: any) {
    console.error(error);
    this.openSnackBar(error, 'close');
  }

  handleCommentUpdateSuccess(input:HTMLTextAreaElement) {
    this.openSnackBar('Comment edited successfully!', 'close');
    input.value = '';
    this.goToBottom();
    this.editedComment = undefined;
  }

  handleCommentAddSuccess(input:HTMLTextAreaElement) {
    this.openSnackBar('Comment added successfully!', 'close');
    input.value = '';
    this.goToBottom();
  }

  goToBottom() {
    const element = document.getElementById('bottom');
    element?.scrollIntoView({ behavior: 'smooth', block: 'end', inline: 'nearest' });
  }

  backToForums() {
    this.forum = undefined;
    this.forumEmitter.emit(this.forum);
  }

  ngOnChanges() {
    this.forumEmitter.emit(this.forum);
    this.goToBottom();
  }

  ngOnDestroy() {
    this.deleteSubscription?.unsubscribe();
    this.commentSubscription?.unsubscribe();
    this.editSubscription?.unsubscribe();
  }
}