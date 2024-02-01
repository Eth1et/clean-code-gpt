import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ExchangeRatesService } from 'src/app/shared/services/exchange-rates.service';
import { Observable, Subscription, map, startWith } from 'rxjs';
import { CryptoCurrency } from 'src/app/shared/models/CryptoCurrency';

@Component({
  selector: 'app-exchange-rates',
  templateUrl: './exchange-rates.component.html',
  styleUrls: ['./exchange-rates.component.scss']
})
export class ExchangeRatesComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['name', 'value'];
  selected: CryptoCurrency = {
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
  initialized = false;

  selectedSubscription?: Subscription;
  optionsSubscription?: Subscription;
  searchSubscription?: Subscription;

  options: string[] = ['Bitcoin', 'Ethereum'];
  filteredOptions?: Observable<string[]>;

  search = new FormControl('');

  constructor(private exchangeRatesService: ExchangeRatesService) {}

  ngOnInit() {
    this.setupListeners();
    this.setDataByName(this.selected.name);
  }

  private setupListeners() {
    this.optionsSubscription = this.exchangeRatesService.getCryptocurrencyNames().subscribe({
      next: queriedOptions => {
        this.updateOptions(queriedOptions);
        this.setupSearchListener();
        this.setupFilterOptions();
      },
      error: error => {
        console.error(error);
      }
    });
  }

  private updateOptions(queriedOptions: string[]) {
    this.options = queriedOptions;
  }

  private setupSearchListener() {
    this.searchSubscription = this.search.valueChanges.subscribe({
      next: searched => {
        this.setDataByName(searched as string);
      },
      error: error => {
        console.error(error);
      }
    });
  }

  private setupFilterOptions() {
    this.filteredOptions = this.search.valueChanges.pipe(
      startWith(''),
      map(name => {
        return name ? this.filterOptions(name) : this.options.slice();
      })
    );
  }

  private filterOptions(name: string): string[] {
    return this.options.filter(option => option.toLowerCase().includes(name.toLowerCase()));
  }

  private setDataByName(name: string) {
    this.selectedSubscription = this.exchangeRatesService.readByName(name).subscribe({
      next: data => {
        this.updateSelected(data, name);
      },
      error: error => {
        console.error(error);
      }
    });
  }

  private updateSelected(data: CryptoCurrency[], name: string) {
    if (data.length > 0 && (!this.initialized || (this.options.indexOf(name) > -1 && name != this.selected.name))) {
      this.selected = data[0];
      this.initialized = true;
    }
  }

  ngOnDestroy() {
    this.unsubscribeAll();
  }

  private unsubscribeAll() {
    this.selectedSubscription?.unsubscribe();
    this.optionsSubscription?.unsubscribe();
    this.searchSubscription?.unsubscribe();
  }
}