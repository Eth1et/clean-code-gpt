import { CustomCurrencyPipe } from './custom-currency.pipe';

describe('CustomCurrencyPipe', () => {
  it('should create an instance', () => {
    // Arrange
    const customCurrencyPipe = new CustomCurrencyPipe();
    
    // Act
    const isInstanceCreated = !!customCurrencyPipe;
    
    // Assert
    expect(isInstanceCreated).toBeTrue();
  });
});