import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { MatAutocompleteModule, MatCardModule, MatDividerModule, MatFormFieldModule, MatIconModule, MatInputModule, MatTableModule } from '@angular/material';
import { FlexLayoutModule } from '@angular/flex-layout';

import { ExchangeRatesComponent } from './exchange-rates.component';
import { ExchangeRatesRoutingModule } from './exchange-rates-routing.module';
import { CustomCurrencyPipe } from 'src/app/shared/pipes/custom-currency.pipe';

@NgModule({
  declarations: [
    ExchangeRatesComponent,
    CustomCurrencyPipe
  ],
  imports: [
    CommonModule,
    ExchangeRatesRoutingModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    MatCardModule,
    MatTableModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatAutocompleteModule,
    MatDividerModule
  ]
})
export class ExchangeRatesModule { }