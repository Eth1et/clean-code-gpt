import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExchangeRatesComponent } from './exchange-rates.component';

const exchangeRoutes: Routes = [{ path: '', component: ExchangeRatesComponent }];

@NgModule({
  imports: [RouterModule.forChild(exchangeRoutes)],
  exports: [RouterModule]
})
export class ExchangeRatesRoutingModule { }