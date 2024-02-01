import { Injectable } from '@angular/core';
import { AngularFirestore, AngularFirestoreCollection, QueryFn } from '@angular/fire/compat/firestore';
import { CryptoCurrency } from '../models/CryptoCurrency';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ExchangeRatesService {

  private readonly collectionName: string = 'CryptoCurrencies';
  private readonly cryptoCurrencyCollection: AngularFirestoreCollection<CryptoCurrency>;

  constructor(private afs: AngularFirestore) {
    this.cryptoCurrencyCollection = this.afs.collection<CryptoCurrency>(this.collectionName);
  }

  readByName(name: string): Observable<CryptoCurrency[]> {
    const query: QueryFn = ref => ref.where('name', '==', name).limit(1);
    return this.afs.collection<CryptoCurrency>(this.collectionName, query).valueChanges();
  }

  getCryptocurrencyNames(): Observable<string[]> {
    return this.cryptoCurrencyCollection.valueChanges().pipe(
      map(cryptoCurrencies => cryptoCurrencies.map(cryptoCurrency => cryptoCurrency.name))
    );
  }

  addCryptocurrency(currency: CryptoCurrency): void {
    this.cryptoCurrencyCollection.doc(currency.abbreviation).set(currency);
  }
}