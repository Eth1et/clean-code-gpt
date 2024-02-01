import { Component, OnDestroy } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { User } from 'src/app/shared/models/User';
import { AuthService } from 'src/app/shared/services/auth.service';
import { UserService } from '../../shared/services/user.service';
import { passwordMatchValidator } from 'src/app/shared/validators/passwords-match';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent implements OnDestroy {
  isLoading = false;
  usernameCheckSubscription?: Subscription;

  signUpForm: FormGroup = this.createSignUpForm();

  constructor(
    private router: Router,
    private authService: AuthService,
    private userService: UserService,
    private snackBar: MatSnackBar
  ) {}

  private createSignUpForm(): FormGroup {
    return new FormGroup({
      username: new FormControl('', [Validators.minLength(3), Validators.maxLength(30), Validators.required]),
      email: new FormControl('', [Validators.email, Validators.required]),
      password: new FormControl('', [Validators.minLength(6), Validators.maxLength(40), Validators.required]),
      rePassword: new FormControl('', [Validators.minLength(6), Validators.maxLength(40), Validators.required]),
      name: new FormGroup({
        firstname: new FormControl('', [Validators.minLength(3), Validators.maxLength(30), Validators.required]),
        lastname: new FormControl('', [Validators.minLength(3), Validators.maxLength(30), Validators.required])
      })
    }, [passwordMatchValidator()]);
  }

  private showSnackBar(message: string): void {
    this.snackBar.open(message, 'close', { duration: 6500 });
  }

  onSubmit(): void {
    const email = this.signUpForm.get('email')?.value;
    const password = this.signUpForm.get('password')?.value;

    if (!this.signUpForm.valid) {
      const errorMessage = this.signUpForm.errors?.['passwordsNotEqual'] ? 
        "Passwords do not match!" : 
        "Fill out all required fields!";
      this.showSnackBar(errorMessage);
      return;
    }

    let isUserCreated = false;

    this.usernameCheckSubscription = this.userService.readByUsername(this.signUpForm.value.username).subscribe({
      next: users => {
        if (users.length === 0) {
          this.createAccount(email, password);
          isUserCreated = true;
        } else if (!isUserCreated) {
          this.showSnackBar("The username is already in use");
        }
      },
      error: error => {
        console.error(error);
        this.showSnackBar(error);
      }
    });
  }

  private createAccount(email: string, password: string): void {
    this.isLoading = true;
    this.authService.signup(email, password)
      .then(credentials => {
        const newUser: User = this.mapFormToUser(credentials);
        return this.userService.create(newUser);
      })
      .then(() => {
        this.router.navigateByUrl('/exchange-rates');
      })
      .catch(error => {
        console.error(error);
        this.showSnackBar(error);
      })
      .finally(() => {
        this.isLoading = false;
      });
  }

  private mapFormToUser(credentials: firebase.auth.UserCredential): User {
    return {
      id: credentials.user?.uid as string,
      email: this.signUpForm.get('email')?.value as string,
      username: this.signUpForm.get('username')?.value as string,
      name: {
        firstname: this.signUpForm.get('name.firstname')?.value as string,
        lastname: this.signUpForm.get('name.lastname')?.value as string
      }
    };
  }

  ngOnDestroy(): void {
    this.usernameCheckSubscription?.unsubscribe();
  }
}