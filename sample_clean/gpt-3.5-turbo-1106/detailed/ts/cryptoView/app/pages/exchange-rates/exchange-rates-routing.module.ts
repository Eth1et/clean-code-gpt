import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ExchangeRatesComponent } from './exchange-rates.component';

const exchangeRatesRoutes: Routes = [{ path: '', component: ExchangeRatesComponent }];

@NgModule({
  imports: [RouterModule.forChild(exchangeRatesRoutes)],
  exports: [RouterModule]
})
export class ExchangeRatesRoutingModule { }