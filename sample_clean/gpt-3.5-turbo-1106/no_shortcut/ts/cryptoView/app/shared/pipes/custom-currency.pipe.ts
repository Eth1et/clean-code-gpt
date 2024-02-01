import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'customCurrency'
})
export class CustomCurrencyPipe implements PipeTransform {
  transform(value: number): string {
    const formattedValue: string = value < 0.001 ? "0.000" : value.toFixed(3);
    const [wholeNumber, decimalPart] = formattedValue.split('.');
    const formattedWholeNumber = wholeNumber.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    const formattedDecimalPart = decimalPart ? decimalPart.slice(0, 3).padEnd(3, "0") : "000";
    return `${formattedWholeNumber}.${formattedDecimalPart}`;
  }
}