import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'customCurrency'
})
export class CustomCurrencyPipe implements PipeTransform {

  transform(value: number): string {
    const formattedValue: string = value < 0.001 ? "0.000" : value.toFixed(3);
    const [wholePart, fractionPart = ""] = formattedValue.split(".");
    const wholeDigits = wholePart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');

    const paddedFractionPart = fractionPart.padEnd(3, "0");

    return wholeDigits + "." + paddedFractionPart;
  }

}