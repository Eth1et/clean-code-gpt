import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'customCurrency'
})
export class CustomCurrencyPipe implements PipeTransform {

  transform(value: number): string {
    const valueString: string = value < 0.001 ? "0.000" : value.toString();
    const [wholePart, fractionPart] = valueString.split('.');
    
    const formattedWholePart = wholePart.match(/.{1,3}(?=(.{3})*$)/g)?.join(',');
    const formattedFractionPart = fractionPart ? fractionPart.slice(0, 3).padEnd(3, '0') : '';

    return `${formattedWholePart}.${formattedFractionPart}`;
  }

}