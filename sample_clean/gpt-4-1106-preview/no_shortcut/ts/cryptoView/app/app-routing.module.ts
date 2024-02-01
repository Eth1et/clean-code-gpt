import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './shared/services/auth.guard';
import { LoggedOutGuard } from './shared/services/logged-out.guard';

function loadModule(path: string) {
  return () => import(`./pages/${path}/${path}.module`).then(m => m[`${capitalize(path)}Module`]);
}

function capitalize(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

const appRoutes: Routes = [
  { path: 'main', loadChildren: loadModule('main') },
  {
    path: 'login',
    canActivate: [LoggedOutGuard],
    loadChildren: loadModule('login')
  },
  {
    path: 'signup',
    canActivate: [LoggedOutGuard],
    loadChildren: loadModule('signup')
  },
  {
    path: 'forum',
    canActivate: [AuthGuard],
    loadChildren: loadModule('forum')
  },
  {
    path: 'exchange-rates',
    canActivate: [AuthGuard],
    loadChildren: loadModule('exchange-rates')
  },
  {
    path: 'profile',
    canActivate: [AuthGuard],
    loadChildren: loadModule('profile')
  },
  { path: 'not-found', loadChildren: loadModule('not-found') },
  { path: '', redirectTo: '/main', pathMatch: 'full' },
  { path: '**', redirectTo: '/not-found' }
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }