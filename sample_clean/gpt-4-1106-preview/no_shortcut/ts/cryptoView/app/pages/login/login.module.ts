import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login.component';
import { MaterialModules } from './material-modules';

@NgModule({
  declarations: [LoginComponent],
  imports: [
    CommonModule,
    LoginRoutingModule,
    ReactiveFormsModule,
    MaterialModules
  ]
})
export class LoginModule { }

// Assuming material-modules.ts is a file that exports an array of the Material modules
// For example:
// material-modules.ts
// import { MatFormFieldModule } from '@angular/material/form-field';
// import { MatInputModule } from '@angular/material/input';
// import { MatButtonModule } from '@angular/material/button';
// import { MatCardModule } from '@angular/material/card';
// import { FlexLayoutModule } from '@angular/flex-layout';
// import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
// import { MatSnackBarModule } from '@angular/material/snack-bar';

// export const MaterialModules = [
//   MatFormFieldModule,
//   MatInputModule,
//   MatSnackBarModule,
//   MatButtonModule,
//   MatCardModule,
//   FlexLayoutModule,
//   MatProgressSpinnerModule
// ];