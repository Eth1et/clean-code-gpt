import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SignupComponent } from './signup.component';

describe('SignupComponent', () => {
  let signupComponent: SignupComponent;
  let fixture: ComponentFixture<SignupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SignupComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SignupComponent);
    signupComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create signup component', () => {
    expect(signupComponent).toBeTruthy();
  });
});