import { ComponentFixture, TestBed } from '@angular/core/testing';
import { SignupComponent } from './signup.component';

describe('SignupComponent Tests', () => {
  let componentUnderTest: SignupComponent;
  let fixture: ComponentFixture<SignupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SignupComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(SignupComponent);
    componentUnderTest = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(componentUnderTest).toBeTruthy();
  });
});