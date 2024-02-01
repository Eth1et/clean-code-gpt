import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'customCurrency'
})
export class CustomCurrencyPipe implements PipeTransform {

  transform(value: number): string {
    const formattedValue = this.formatNumber(value);
    return formattedValue;
  }

  private formatNumber(value: number): string {
    const num: string = value < 0.001 ? "0.000" : value.toString();
    const [wholeDigits, fractionDigits] = this.splitNumber(num);
    const formattedFraction = this.formatFractionDigits(fractionDigits);
    return wholeDigits + "." + formattedFraction;
  }

  private splitNumber(num: string): [string, string] {
    const parts = num.split('.');
    const wholeDigits = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    const fractionDigits = parts[1] || "";
    return [wholeDigits, fractionDigits];
  }

  private formatFractionDigits(fractionDigits: string): string {
    return fractionDigits ? fractionDigits.slice(0, 3).padEnd(3, "0") : "000";
  }
}