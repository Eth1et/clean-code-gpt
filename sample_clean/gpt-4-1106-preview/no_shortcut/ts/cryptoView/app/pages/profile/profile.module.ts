import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProfileRoutingModule } from './profile-routing.module';
import { ProfileComponent } from './profile.component';
import { MaterialModules } from './material-modules';

@NgModule({
  declarations: [ProfileComponent],
  imports: [
    CommonModule,
    ProfileRoutingModule,
    ...MaterialModules
  ]
})
export class ProfileModule { }

// material-modules.ts (new file)
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatDividerModule } from '@angular/material/divider';

export const MaterialModules = [
  MatIconModule,
  MatCardModule,
  MatSnackBarModule,
  FlexLayoutModule,
  MatDividerModule
];