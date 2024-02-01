import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ForumComponent } from './forum.component';

describe('ForumComponent', () => {
  let forumComponent: ForumComponent;
  let forumFixture: ComponentFixture<ForumComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ForumComponent ]
    }).compileComponents();

    forumFixture = TestBed.createComponent(ForumComponent);
    forumComponent = forumFixture.componentInstance;
    forumFixture.detectChanges();
  });

  it('should create forum component', () => {
    expect(forumComponent).toBeTruthy();
  });
});