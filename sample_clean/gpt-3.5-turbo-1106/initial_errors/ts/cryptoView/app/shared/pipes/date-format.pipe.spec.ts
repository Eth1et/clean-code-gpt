import { DateFormatPipe } from './date-format.pipe';

describe('DateFormatPipe', () => {
  it('should create an instance of DateFormatPipe', () => {
    // Arrange
    const pipe = new DateFormatPipe();
    
    // Act & Assert
    expect(pipe).toBeTruthy();
  });
});