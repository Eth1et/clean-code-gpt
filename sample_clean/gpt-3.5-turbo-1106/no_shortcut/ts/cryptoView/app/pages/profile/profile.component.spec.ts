import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ProfileComponent } from './profile.component';

describe('ProfileComponent', () => {
  let profileComponent: ProfileComponent;
  let fixture: ComponentFixture<ProfileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProfileComponent ]
    }).compileComponents();

    fixture = TestBed.createComponent(ProfileComponent);
    profileComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create profile component', () => {
    expect(profileComponent).toBeTruthy();
  });
});