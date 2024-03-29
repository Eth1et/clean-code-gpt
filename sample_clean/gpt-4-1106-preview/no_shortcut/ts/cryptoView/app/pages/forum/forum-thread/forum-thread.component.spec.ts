import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ForumThreadComponent } from './forum-thread.component';

describe('ForumThreadComponent Unit Tests', () => {
  let component: ForumThreadComponent;
  let fixture: ComponentFixture<ForumThreadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ForumThreadComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ForumThreadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should instantiate the component', () => {
    expect(component).toBeDefined();
  });
});