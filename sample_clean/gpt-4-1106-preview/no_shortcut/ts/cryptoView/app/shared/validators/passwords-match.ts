import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function PasswordMatchValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const password = control.get('password')?.value;
    const confirmPassword = control.get('rePassword')?.value;

    if (password && confirmPassword && password !== confirmPassword) {
      control.get('rePassword')?.setErrors({ passwordsNotEqual: true });
    }

    return password !== confirmPassword ? { passwordsNotEqual: true } : null;
  };
}