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

  forums: Forum[] | undefined;
  forumSubscription: Subscription | undefined;
  selectedForum: Forum | undefined;

  constructor(private forumService: ForumService) {}

  ngOnInit(): void {
    this.forumSubscription = this.forumService.readAll().subscribe({
      next: (forums: Forum[]) => {
        this.forums = forums;
      },
      error: (error: any) => {
        console.error(error);
      }
    });
  }

  emittedForum(forum: Forum): void {
    this.selectedForum = forum;
  }

  selectForum(forum: Forum): void {
    this.selectedForum = forum;
  }

  ngOnDestroy(): void {
    this.forumSubscription?.unsubscribe();
  }
}