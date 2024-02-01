import { 
  Component, 
  OnInit, 
  OnDestroy, 
  Input 
} from '@angular/core';
import { 
  FormControl 
} from '@angular/forms';
import { 
  ExchangeRatesService 
} from 'src/app/shared/services/exchange-rates.service';
import { 
  Observable, 
  Subscription, 
  map, 
  startWith 
} from 'rxjs';
import { 
  CryptoCurrency 
} from 'src/app/shared/models/CryptoCurrency';

@Component({
  selector: 'app-exchange-rates',
  templateUrl: './exchange-rates.component.html',
  styleUrls: ['./exchange-rates.component.scss']
})
export class ExchangeRatesComponent implements OnInit, OnDestroy {
  displayedColumns: string[] = ['name', 'value'];
  selectedCrypto: CryptoCurrency = {
    name: 'Bitcoin',
    abbreviation: 'BTC',
    values:[
      {
        name: 'US Dollar',
        abbreviation: 'USD',
        value: 29942.79
      }
    ]
  };
  isInitialized = false;
  
  selectedSubscription?: Subscription;
  optionsSubscription?: Subscription;
  searchSubscription?: Subscription;

  optionsList: string[] = ['Bitcoin', 'Ethereum'];
  filteredOptions?: Observable<string[]>;

  searchInput =  new FormControl('');

  constructor(private exchangeRatesService: ExchangeRatesService) {}

  ngOnInit() {
    this.loadDataForSelectedCrypto(this.selectedCrypto.name);
    this.handleOptionsSubscription();
  }

  private handleOptionsSubscription() {
    this.optionsSubscription = this.exchangeRatesService
      .getCryptocurrencyNames()
      .subscribe({
        next: queriedOptions => {
          this.optionsList = queriedOptions;
          this.setupSearchSubscription();
          this.filteredOptions = this.searchInput.valueChanges.pipe(
            startWith(''),
            map(name => this.filterOptions(name)),
          );
        },
        error: error => {
          console.error(error);
        }
      });
  }

  private setupSearchSubscription() {
    this.searchSubscription = this.searchInput.valueChanges.subscribe({
      next: searched => {
        this.loadDataForSelectedCrypto(searched as string);
      },
      error: error => {
        console.error(error);
      }
    });
  }

  private filterOptions(name: string): string[] {
    return this.optionsList
      .filter(option => option.toLowerCase().includes(name.toLowerCase()));
  }

  private loadDataForSelectedCrypto(name: string){
    this.selectedSubscription = this.exchangeRatesService.readByName(name).subscribe({
      next: data => {
        if(data.length > 0 && (!this.isInitialized || (this.optionsList.indexOf(name) > -1 && name != this.selectedCrypto.name))){
          this.selectedCrypto = data[0];
          this.isInitialized = true;
        }
      },
      error: error => {
        console.error(error);
      }
    });
  }

  ngOnDestroy() {
    this.selectedSubscription?.unsubscribe();
    this.optionsSubscription?.unsubscribe();
    this.searchSubscription?.unsubscribe();
  }
}