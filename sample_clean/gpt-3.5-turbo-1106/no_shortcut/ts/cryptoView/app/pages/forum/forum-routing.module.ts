import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ForumComponent } from './forum.component';

const forumRoutes: Routes = [{ path: '', component: ForumComponent }];

@NgModule({
  imports: [RouterModule.forChild(forumRoutes)],
  exports: [RouterModule]
})
export class ForumRoutingModule { 

}