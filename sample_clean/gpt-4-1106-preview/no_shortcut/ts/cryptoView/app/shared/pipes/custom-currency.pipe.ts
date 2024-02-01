import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'customCurrency'
})
export class CustomCurrencyPipe implements PipeTransform {
  transform(amount: number): string {
    const formattedAmountThreshold = 0.001;
    const fractionDigitsRequired = 3;
    
    let amountString = amount < formattedAmountThreshold ? "0.000" : amount.toFixed(fractionDigitsRequired);
    let [wholePart, fractionPart] = amountString.split('.');
    wholePart = this.formatWholePartWithCommas(wholePart);
    fractionPart = this.padFractionalPart(fractionPart, fractionDigitsRequired);

    return `${wholePart}.${fractionPart}`;
  }

  private formatWholePartWithCommas(wholePart: string): string {
    const regex = /(\d)(?=(\d{3})+(?!\d))/g;
    return wholePart.replace(regex, '$1,');
  }

  private padFractionalPart(fractionPart: string, length: number): string {
    return fractionPart.padEnd(length, '0');
  }
}