import { Component, OnDestroy, OnInit } from '@angular/core';
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

  ngOnInit(): void {
    this.initializeData();
    this.initializeSubscriptions();
  }

  private initializeData(): void {
    this.setDataByName(this.selected.name);
  }

  private initializeSubscriptions(): void {
    this.optionsSubscription = this.exchangeRatesService.getCryptocurrencyNames().subscribe({
      next: queriedOptions => {
        this.options = queriedOptions;
        this.handleSearchSubscription();
        this.setFilteredOptions();
      },
      error: error => {
        console.error(error);
      }
    });
  }

  private handleSearchSubscription(): void {
    this.searchSubscription?.unsubscribe();
    this.searchSubscription = this.search.valueChanges.subscribe({
      next: searched => {
        this.setDataByName(searched as string);
      },
      error: error => {
        console.error(error);
      }
    });
  }

  private setFilteredOptions(): void {
    this.filteredOptions = this.search.valueChanges.pipe(
      startWith(''),
      map(name => this.filterOptions(name))
    );
  }

  private filterOptions(name: string): string[] {
    return this.options.filter(option => option.toLowerCase().includes(name.toLowerCase()));
  }

  setDataByName(name: string): void {
    this.selectedSubscription?.unsubscribe();
    this.selectedSubscription = this.exchangeRatesService.readByName(name).subscribe({
      next: data => {
        this.updateSelected(data, name);
      },
      error: error => {
        console.error(error);
      }
    });
  }

  private updateSelected(data: CryptoCurrency[], name: string): void {
    if (data.length > 0 && (!this.initialized || (this.options.includes(name) && name !== this.selected.name))) {
      this.selected = data[0];
      this.initialized = true;
    }
  }

  ngOnDestroy(): void {
    this.unsubscribeFromSubscriptions();
  }

  private unsubscribeFromSubscriptions(): void {
    this.selectedSubscription?.unsubscribe();
    this.optionsSubscription?.unsubscribe();
    this.searchSubscription?.unsubscribe();
  }
}