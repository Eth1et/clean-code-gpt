import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExchangeRatesComponent } from './exchange-rates.component';

describe('ExchangeRatesComponent', () => {
  let exchangeRatesComponent: ExchangeRatesComponent;
  let fixture: ComponentFixture<ExchangeRatesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ExchangeRatesComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExchangeRatesComponent);
    exchangeRatesComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create component', () => {
    expect(exchangeRatesComponent).toBeTruthy();
  });
});