import { Injectable } from '@angular/core';
import { AngularFirestore, DocumentData } from '@angular/fire/compat/firestore';
import { CryptoCurrency } from '../models/CryptoCurrency';
import { Observable } from 'rxjs';
import { map, first } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ExchangeRatesService {

  private readonly collectionName: string = 'CryptoCurrencies';

  constructor(private readonly angularFirestore: AngularFirestore) { }

  public readByName(name: string): Observable<CryptoCurrency[]> {
    return this.angularFirestore.collection<CryptoCurrency>(this.collectionName, ref => ref.where('name', '==', name).limit(1))
      .valueChanges();
  }

  public getCryptocurrencyNames(): Observable<string[]> {
    return this.angularFirestore.collection<CryptoCurrency>(this.collectionName).valueChanges()
      .pipe(
        map((docs: CryptoCurrency[]) => docs.map((currency: CryptoCurrency) => currency.name))
      );
  }

  public addCryptocurrency(currency: CryptoCurrency): void {
    this.angularFirestore.collection<CryptoCurrency>(this.collectionName).doc(currency.abbreviation).set({ ...currency });
  }
}