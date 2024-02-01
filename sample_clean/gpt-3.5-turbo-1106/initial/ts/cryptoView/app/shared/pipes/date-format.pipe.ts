import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dateFormat'
})
export class DateFormatPipe implements PipeTransform {

  transform(value: number, ...args: unknown[]): string {
    const date = new Date(value);
    const formattedDate = this.getFormattedDate(date);
    const formattedTime = this.getFormattedTime(date);
    return `${formattedDate} ${formattedTime}`;
  }

  private getFormattedDate(date: Date): string {
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
  }

  private getFormattedTime(date: Date): string {
    return date.toLocaleTimeString("en-US", { hour: "numeric", minute: "numeric", hour12: true });
  }
}