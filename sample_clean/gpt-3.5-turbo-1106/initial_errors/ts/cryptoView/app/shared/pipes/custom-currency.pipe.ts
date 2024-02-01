import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'customCurrency'
})
export class CustomCurrencyPipe implements PipeTransform {

  transform(value: number): string {
    const formattedValue = formatCurrency(value);
    return formattedValue;
  }

  private formatCurrency(value: number): string {
    const numString: string = value.toFixed(3);
    const parts: string[] = numString.split('.');
    const wholeDigits: string = this.groupDigits(parts[0]);
    const fractionDigits: string = this.truncateFraction(parts[1]);
    return `${wholeDigits}.${fractionDigits}`;
  }

  private groupDigits(digits: string): string {
    return digits.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  private truncateFraction(digits: string): string {
    if (digits) {
      return digits.slice(0, 3).padEnd(3, '0');
    }
    return '000';
  }
}