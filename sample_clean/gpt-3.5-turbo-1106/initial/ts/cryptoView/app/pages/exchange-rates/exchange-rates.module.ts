import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatTableModule } from '@angular/material/table';
import { MatDividerModule } from '@angular/material/divider';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { ExchangeRatesRoutingModule } from './exchange-rates-routing.module';
import { ExchangeRatesComponent } from './exchange-rates.component';
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