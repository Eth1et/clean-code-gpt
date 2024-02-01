import { CustomCurrencyPipe } from './custom-currency.pipe';

describe('CustomCurrencyPipe', () => {
  let customCurrencyPipe: CustomCurrencyPipe;

  beforeEach(() => {
    customCurrencyPipe = new CustomCurrencyPipe();
  });

  it('should create an instance', () => {
    expect(customCurrencyPipe).toBeTruthy();
  });
});