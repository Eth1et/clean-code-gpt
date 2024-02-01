import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './shared/services/auth.guard';
import { LoggedOutGuard } from './shared/services/logged-out.guard';
import { MainModule } from './pages/main/main.module';
import { LoginModule } from './pages/login/login.module';
import { SignupModule } from './pages/signup/signup.module';
import { ForumModule } from './pages/forum/forum.module';
import { ExchangeRatesModule } from './pages/exchange-rates/exchange-rates.module';
import { ProfileModule } from './pages/profile/profile.module';
import { NotFoundModule } from './pages/not-found/not-found.module';

const routes: Routes = [
  { path: 'main', loadChildren: () => import('./pages/main/main.module').then(m => m.MainModule) },
  { path: 'login', canActivate: [LoggedOutGuard], loadChildren: () => import('./pages/login/login.module').then(m => m.LoginModule) },
  { path: 'signup', canActivate: [LoggedOutGuard], loadChildren: () => import('./pages/signup/signup.module').then(m => m.SignupModule) },
  { path: 'forum', canActivate: [AuthGuard], loadChildren: () => import('./pages/forum/forum.module').then(m => m.ForumModule) },
  { path: 'exchange-rates', canActivate: [AuthGuard], loadChildren: () => import('./pages/exchange-rates/exchange-rates.module').then(m => m.ExchangeRatesModule) },
  { path: 'profile', canActivate: [AuthGuard], loadChildren: () => import('./pages/profile/profile.module').then(m => m.ProfileModule) },
  { path: 'not-found', loadChildren: () => import('./pages/not-found/not-found.module').then(m => m.NotFoundModule) },
  { path: '', redirectTo: '/main', pathMatch: 'full' },
  { path: '**', redirectTo: '/not-found' },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }