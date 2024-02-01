import { ComponentFixture, TestBed } from '@angular/core/testing';
import { LoginComponent } from './login.component';

describe('LoginComponent', () => {
  let loginComponent: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LoginComponent ]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    loginComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create login component', () => {
    expect(loginComponent).toBeTruthy();
  });
});