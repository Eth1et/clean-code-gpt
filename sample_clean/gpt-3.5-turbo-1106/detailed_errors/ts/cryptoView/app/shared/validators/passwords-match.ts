import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function passwordMatchValidator(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const passwordControl = control.get('password');
    const rePasswordControl = control.get('rePassword');

    if (passwordControl?.value && rePasswordControl?.value && passwordControl.value !== rePasswordControl.value) {
      rePasswordControl.setErrors({ passwordsNotEqual: true });
      return { passwordsNotEqual: true };
    }

    return null;
  };
}