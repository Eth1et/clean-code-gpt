import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/shared/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {
  emailFormControl = new FormControl('', [Validators.email, Validators.required]);
  passwordFormControl = new FormControl('', [Validators.minLength(6), Validators.maxLength(40), Validators.required]);

  isLoading = false;

  constructor(
    private router: Router,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) {}

  private showSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, { duration: 4000 });
  }

  onLogin() {
    if (this.isLoading) return;

    this.isLoading = true;
    const email = this.emailFormControl.value as string;
    const password = this.passwordFormControl.value as string;

    this.authService.login(email, password).then(() => {
      this.router.navigateByUrl('/exchange-rates');
    }).catch(error => {
      console.error(error);
      this.showSnackBar("Incorrect email or password!", "Close");
    }).finally(() => {
      this.isLoading = false;
    });
  }
}