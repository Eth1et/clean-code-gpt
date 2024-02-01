import { DateFormatPipe } from './date-format.pipe';

describe('DateFormatPipe', () => {
  let dateFormatPipe: DateFormatPipe;

  beforeEach(() => {
    dateFormatPipe = new DateFormatPipe();
  });

  it('should create an instance', () => {
    expect(dateFormatPipe).toBeTruthy();
  });
});