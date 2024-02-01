import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

// Material Modules
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';

// Flex Layout Module
import { FlexLayoutModule } from '@angular/flex-layout';

// Routing and Components
import { ForumRoutingModule } from './forum-routing.module';
import { ForumComponent } from './forum.component';
import { ForumThreadComponent } from './forum-thread/forum-thread.component';

// Pipes
import { DateFormatPipe } from 'src/app/shared/pipes/date-format.pipe';

@NgModule({
  declarations: [
    ForumComponent,
    ForumThreadComponent,
    DateFormatPipe
  ],
  imports: [
    CommonModule,
    ForumRoutingModule,
    MatCardModule,
    MatIconModule,
    MatSnackBarModule,
    ReactiveFormsModule,
    MatInputModule,
    FlexLayoutModule,
    MatButtonModule,
    MatDividerModule
  ]
})
export class ForumModule { }