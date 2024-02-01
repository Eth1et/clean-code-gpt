import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'customCurrency'
})
export class CustomCurrencyPipe implements PipeTransform {

  transform(value: number): string {
    const numString: string = value.toFixed(3);
    const [wholeDigits, fractionDigits] = numString.split('.');
    const formattedWholeDigits = wholeDigits.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    const formattedFractionDigits = fractionDigits || '000';
    return `${formattedWholeDigits}.${formattedFractionDigits.slice(0, 3)}`;
  }

}