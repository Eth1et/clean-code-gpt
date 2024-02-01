import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { ForumComponent } from './forum.component';

const forumRoutes = [
  { path: '', component: ForumComponent }
];

@NgModule({
  imports: [RouterModule.forChild(forumRoutes)],
  exports: [RouterModule]
})
export class ForumRoutingModule { }