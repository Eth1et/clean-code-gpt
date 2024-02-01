import { Injectable } from '@angular/core';
import { AngularFirestore, AngularFirestoreDocument, QueryFn } from '@angular/fire/compat/firestore';
import { CryptoCurrency } from '../models/CryptoCurrency';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ExchangeRatesService {

  private readonly collectionName: string = 'CryptoCurrencies';

  constructor(private firestore: AngularFirestore) { }

  public readByName(name: string): Observable<CryptoCurrency[]> {
    return this.firestore.collection<CryptoCurrency>(this.collectionName, query => this.queryByName(name, query))
      .valueChanges();
  }

  private queryByName(name: string, query: QueryFn): QueryFn {
    return query.where('name', '==', name).limit(1);
  }

  public getCryptocurrencyNames(): Observable<string[]> {
    return this.firestore.collection<CryptoCurrency>(this.collectionName).valueChanges()
      .pipe(
        map(currencies => currencies.map(currency => currency.name))
      );
  }

  public addCryptocurrency(currency: CryptoCurrency): void {
    const currencyDocument: AngularFirestoreDocument<CryptoCurrency> = this.firestore.collection<CryptoCurrency>(this.collectionName).doc(currency.abbreviation);
    currencyDocument.set(currency);
  }
}