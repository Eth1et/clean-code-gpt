import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ForumComponent } from './forum.component';

describe('ForumComponent Unit Tests', () => {
  let forumComponent: ForumComponent;
  let fixture: ComponentFixture<ForumComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ForumComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ForumComponent);
    forumComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created successfully', () => {
    expect(forumComponent).toBeTruthy();
  });
});