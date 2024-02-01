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
  isLoading: boolean = false;

  constructor(private router: Router, private authService: AuthService, private snackBar: MatSnackBar) {}

  openSnackBar(message: string, action: string): void {
    this.snackBar.open(message, action, { duration: 4000 });
  }

  login(): void {
    this.isLoading = true;
    this.authService.login(this.emailFormControl.value as string, this.passwordFormControl.value as string)
      .then(cred => {
        this.router.navigateByUrl('/exchange-rates');
      })
      .catch(err => {
        console.error(err);
        this.openSnackBar("Incorrect email or password!", "close");
      })
      .finally(() => {
        this.isLoading = false;
      });
  }
}