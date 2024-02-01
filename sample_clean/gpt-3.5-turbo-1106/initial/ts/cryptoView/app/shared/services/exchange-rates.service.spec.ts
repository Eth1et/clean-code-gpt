import { TestBed } from '@angular/core/testing';

import { ExchangeRatesService } from './exchange-rates.service';

describe('ExchangeRatesService', () => {
  let exchangeRatesService: ExchangeRatesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    exchangeRatesService = TestBed.inject(ExchangeRatesService);
  });

  it('should be created', () => {
    expect(exchangeRatesService).toBeTruthy();
  });
});