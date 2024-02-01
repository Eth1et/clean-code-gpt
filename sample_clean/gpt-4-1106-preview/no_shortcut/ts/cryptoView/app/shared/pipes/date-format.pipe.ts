import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'dateFormat'
})
export class DateFormatPipe implements PipeTransform {
  transform(value: number): string {
    const date = new Date(value);
    const options = { 
      month: "short", 
      day: "numeric", 
      year: "numeric", 
      hour: "numeric", 
      minute: "numeric", 
      hour12: true 
    };
    
    return date.toLocaleDateString("en-US", options) + ' ' + date.toLocaleTimeString("en-US", options);
  }
}