import { Injectable } from '@angular/core';
import { AngularFirestore, DocumentChangeAction } from '@angular/fire/compat/firestore';
import { CryptoCurrency } from '../models/CryptoCurrency';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ExchangeRatesService {
  private collectionName: string = 'CryptoCurrencies';

  constructor(private afs: AngularFirestore) { }

  getCryptoCurrencyByName(name: string): Observable<CryptoCurrency[]> {
    return this.afs.collection<CryptoCurrency>(this.collectionName, ref => ref.where('name', '==', name).limit(1)).valueChanges();
  }

  getCryptoCurrencyNames(): Observable<string[]> {
    return this.afs.collection<CryptoCurrency>(this.collectionName).valueChanges()
      .pipe(
        map((docs: CryptoCurrency[]) => docs.map((doc: CryptoCurrency) => doc.name))
      );
  }

  addCryptoCurrency(currency: CryptoCurrency): void {
    this.afs.collection<CryptoCurrency>(this.collectionName).doc(currency.abbreviation).set(currency);
  }
}