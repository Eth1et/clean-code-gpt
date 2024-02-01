import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { CryptoCurrency } from '../models/CryptoCurrency';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ExchangeRatesService {
  private readonly currencyCollection = 'CryptoCurrencies';

  constructor(private firestore: AngularFirestore) { }

  getCryptoCurrencyByName(name: string): Observable<CryptoCurrency[]> {
    return this.firestore
      .collection<CryptoCurrency>(this.currencyCollection, ref => ref.where('name', '==', name).limit(1))
      .valueChanges();
  }

  getAllCryptoCurrencyNames(): Observable<string[]> {
    return this.firestore
      .collection<CryptoCurrency>(this.currencyCollection)
      .valueChanges()
      .pipe(map(currencies => currencies.map(currency => currency.name)));
  }

  saveCryptoCurrency(currency: CryptoCurrency): void {
    this.firestore
      .collection<CryptoCurrency>(this.currencyCollection)
      .doc(currency.abbreviation)
      .set(currency);
  }
}