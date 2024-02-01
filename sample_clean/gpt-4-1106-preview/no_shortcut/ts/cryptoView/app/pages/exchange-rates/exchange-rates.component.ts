import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ExchangeRatesService } from 'src/app/shared/services/exchange-rates.service';
import { Observable, Subscription } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { CryptoCurrency } from 'src/app/shared/models/CryptoCurrency';

@Component({
  selector: 'app-exchange-rates',
  templateUrl: './exchange-rates.component.html',
  styleUrls: ['./exchange-rates.component.scss']
})
export class ExchangeRatesComponent implements OnInit, OnDestroy {
  displayedColumns = ['name', 'value'];
  selectedCurrency: CryptoCurrency = {
    name: 'Bitcoin',
    abbreviation: 'BTC',
    values: [
      {
        name: 'US Dollar',
        abbreviation: 'USD',
        value: 29942.79
      }
    ]
  };
  isCurrencySelected = false;
  
  cryptocurrencyNamesSubscription?: Subscription;
  currencyValueSubscription?: Subscription;
  searchValueSubscription?: Subscription;

  cryptocurrencyOptions: string[] = ['Bitcoin', 'Ethereum'];
  filteredCryptocurrencyOptions?: Observable<string[]>;

  searchControl = new FormControl('');

  constructor(private exchangeRatesService: ExchangeRatesService) {}

  ngOnInit() {
    this.initializeSelectedCurrencyData();

    this.cryptocurrencyNamesSubscription = this.getCryptocurrencyNames();
  }

  private initializeSelectedCurrencyData() {
    this.fetchCurrencyData(this.selectedCurrency.name);
  }

  private getCryptocurrencyNames(): Subscription {
    return this.exchangeRatesService.getCryptocurrencyNames().subscribe({
      next: (options) => {
        this.cryptocurrencyOptions = options;
        this.initializeSearchSubscription();
        this.initializeFilteredOptions();
      },
      error: console.error
    });
  }

  private initializeSearchSubscription() {
    this.searchValueSubscription = this.searchControl.valueChanges.subscribe({
      next: (value) => this.fetchCurrencyData(value),
      error: console.error
    });
  }

  private initializeFilteredOptions() {
    this.filteredCryptocurrencyOptions = this.searchControl.valueChanges.pipe(
      startWith(''),
      map(value => this.filterOptions(value))
    );
  }

  private filterOptions(value: string): string[] {
    const filterValue = value.toLowerCase();
    return this.cryptocurrencyOptions.filter(option =>
      option.toLowerCase().includes(filterValue)
    );
  }

  private fetchCurrencyData(currencyName: string) {
    this.currencyValueSubscription = this.exchangeRatesService.readByName(currencyName).subscribe({
      next: (currencyData) => {
        if (this.isNewCurrencySelected(currencyData, currencyName)) {
          this.selectedCurrency = currencyData[0];
          this.isCurrencySelected = true;
        }
      },
      error: console.error
    });
  }

  private isNewCurrencySelected(currencyData: CryptoCurrency[], currencyName: string): boolean {
    return currencyData.length > 0 && 
    (!this.isCurrencySelected ||
      (this.cryptocurrencyOptions.includes(currencyName) && currencyName !== this.selectedCurrency.name));
  }

  ngOnDestroy() {
    this.cryptocurrencyNamesSubscription?.unsubscribe();
    this.currencyValueSubscription?.unsubscribe();
    this.searchValueSubscription?.unsubscribe();
  }
}