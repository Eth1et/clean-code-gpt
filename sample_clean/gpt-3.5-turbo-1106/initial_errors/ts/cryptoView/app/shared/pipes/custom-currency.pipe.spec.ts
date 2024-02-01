import { CustomCurrencyPipe } from './custom-currency.pipe';

describe('CustomCurrencyPipe', () => {
  let pipe: CustomCurrencyPipe;

  beforeEach(() => {
    pipe = new CustomCurrencyPipe();
  });

  it('should create an instance', () => {
    expect(pipe).toBeTruthy();
  });
});