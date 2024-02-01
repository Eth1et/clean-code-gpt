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
  loading = false;

  constructor(private router: Router, private authService: AuthService, private snackBar: MatSnackBar) {}

  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, { duration: 4000 });
  }

  async login() {
    this.loading = true;
    try {
      await this.authService.login(this.emailFormControl.value as string, this.passwordFormControl.value as string);
      this.router.navigateByUrl('/exchange-rates');
    } catch (error) {
      console.error(error);
      this.openSnackBar('Incorrect email or password!', 'close');
    } finally {
      this.loading = false;
    }
  }
}