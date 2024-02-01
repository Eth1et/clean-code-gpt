import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './shared/services/auth.guard';
import { LoggedOutGuard } from './shared/services/logged-out.guard';

const routes: Routes = [
  { path: 'main', loadChildren: () => import('./pages/main/main.module').then(module => module.MainModule) },
  { path: 'login', canActivate: [LoggedOutGuard], loadChildren: () => import('./pages/login/login.module').then(module => module.LoginModule) },
  { path: 'signup', canActivate: [LoggedOutGuard], loadChildren: () => import('./pages/signup/signup.module').then(module => module.SignupModule) },
  { path: 'forum', canActivate: [AuthGuard], loadChildren: () => import('./pages/forum/forum.module').then(module => module.ForumModule) },
  { path: 'exchange-rates', canActivate: [AuthGuard], loadChildren: () => import('./pages/exchange-rates/exchange-rates.module').then(module => module.ExchangeRatesModule) },
  { path: 'profile', canActivate: [AuthGuard], loadChildren: () => import('./pages/profile/profile.module').then(module => module.ProfileModule) },
  { path: 'not-found', loadChildren: () => import('./pages/not-found/not-found.module').then(module => module.NotFoundModule) },
  { path: '', redirectTo: '/main', pathMatch: 'full' },
  { path: '**', redirectTo: '/not-found' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }