import { TestBed } from '@angular/core/testing';
import { LoggedOutGuard } from './logged-out.guard';

describe('LoggedOutGuard', () => {
  let loggedOutGuard: LoggedOutGuard;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    loggedOutGuard = TestBed.inject(LoggedOutGuard);
  });

  it('should be created', () => {
    expect(loggedOutGuard).toBeTruthy();
  });
});