import { DateFormatPipe } from './date-format.pipe';

describe('DateFormatPipe', () => {
  it('should create an instance of DateFormatPipe', () => {
    // Arrange
    const dateFormatPipe = new DateFormatPipe();

    // Act
    const result = dateFormatPipe;

    // Assert
    expect(result).toBeTruthy();
  });
});