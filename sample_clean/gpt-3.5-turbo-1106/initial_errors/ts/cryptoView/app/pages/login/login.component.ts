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
  email = new FormControl('', [Validators.email, Validators.required]);
  password = new FormControl('', [Validators.minLength(6), Validators.maxLength(40), Validators.required]);
  loading = false;

  constructor(private router: Router, private authService: AuthService, private snackBar: MatSnackBar) {}

  openSnackBar(message: string, action: string): void {
    this.snackBar.open(message, action, { duration: 4000 });
  }

  async login(): Promise<void> {
    this.loading = true;
    try {
      await this.authService.login(this.email.value as string, this.password.value as string);
      this.router.navigateByUrl('/exchange-rates');
    } catch (error) {
      console.error(error);
      this.openSnackBar('Incorrect email or password!', 'close');
    } finally {
      this.loading = false;
    }
  }
}