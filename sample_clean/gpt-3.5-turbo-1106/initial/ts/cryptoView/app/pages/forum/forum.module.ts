import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ForumRoutingModule } from './forum-routing.module';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { FlexLayoutModule } from '@angular/flex-layout';

import { ForumComponent } from './forum.component';
import { ForumThreadComponent } from './forum-thread/forum-thread.component';
import { DateFormatPipe } from 'src/app/shared/pipes/date-format.pipe';

@NgModule({
  declarations: [
    ForumComponent,
    ForumThreadComponent,
    DateFormatPipe
  ],
  imports: [
    CommonModule,
    FormsModule,
    ForumRoutingModule,
    MatCardModule,
    MatIconModule,
    MatSnackBarModule,
    MatInputModule,
    MatButtonModule,
    FlexLayoutModule
  ]
})
export class ForumModule { }