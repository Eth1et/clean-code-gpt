import { TestBed } from '@angular/core/testing';
import { LoggedOutGuard } from './logged-out.guard';

describe('LoggedOutGuard', () => {
  let guard: LoggedOutGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    guard = TestBed.inject(LoggedOutGuard);
  });

  it('should be created', () => {
    const isLoggedIn = guard.canActivate();
    expect(isLoggedIn).toBeTruthy();
  });
});