import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'customCurrency'
})
export class CustomCurrencyPipe implements PipeTransform {

  transform(value: number): string {
    const formattedValue: string = value < 0.001 ? "0.000" : value.toString();
    const [wholeNumber, decimalNumber] = formattedValue.split('.');
    
    const formattedWholeNumber = wholeNumber.match(/.{1,3}(?=(.{3})*$)/g)?.join(',');
    
    let formattedDecimalNumber = decimalNumber ? decimalNumber.slice(0, 3) : '';
    formattedDecimalNumber = formattedDecimalNumber.padEnd(3, '0');
    
    return `${formattedWholeNumber}.${formattedDecimalNumber}`;
  }

}