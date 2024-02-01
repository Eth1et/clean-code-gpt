import { Component, OnInit, OnDestroy } from '@angular/core';
import { Forum } from 'src/app/shared/models/Forum';
import { ForumService } from 'src/app/shared/services/forum.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-forum',
  templateUrl: './forum.component.html',
  styleUrls: ['./forum.component.scss']
})
export class ForumComponent implements OnInit, OnDestroy {
  forums: Forum[];
  private subscription: Subscription;
  currentForum: Forum;

  constructor(private forumService: ForumService) {}

  ngOnInit(): void {
    this.subscribeToForums();
  }

  private subscribeToForums(): void {
    this.subscription = this.forumService.readAll().subscribe({
      next: forums => (this.forums = forums),
      error: error => console.error(error),
    });
  }

  onForumSelected(forum: Forum): void {
    this.currentForum = forum;
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}