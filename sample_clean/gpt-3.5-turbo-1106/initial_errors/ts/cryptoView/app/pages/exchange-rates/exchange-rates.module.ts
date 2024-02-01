import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ExchangeRatesRoutingModule } from './exchange-rates-routing.module';
import { 
  MatCardModule,
  MatAutocompleteModule,
  MatTableModule,
  MatDividerModule,
  MatFormFieldModule,
  MatInputModule,
  MatIconModule
} from '@angular/material';
import { ExchangeRatesComponent } from './exchange-rates.component';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ReactiveFormsModule } from '@angular/forms';
import { CustomCurrencyPipe } from 'src/app/shared/pipes/custom-currency.pipe';

@NgModule({
  declarations: [
    ExchangeRatesComponent,
    CustomCurrencyPipe
  ],
  imports: [
    CommonModule,
    ExchangeRatesRoutingModule,
    MatCardModule,
    MatAutocompleteModule,
    MatTableModule,
    MatDividerModule,
    FlexLayoutModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule,
    MatIconModule
  ]
})
export class ExchangeRatesModule { }