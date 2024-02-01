import { TestBed } from '@angular/core/testing';
import { ForumService } from './forum.service';

describe('ForumService', () => {
  let forumService: ForumService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    forumService = TestBed.inject(ForumService);
  });

  it('should be created', () => {
    expect(forumService).toBeTruthy();
  });
});