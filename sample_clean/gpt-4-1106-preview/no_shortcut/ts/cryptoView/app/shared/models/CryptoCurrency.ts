import { CurrencyValue } from "./CurrencyValue";

export interface Cryptocurrency {
    name: string;
    abbreviation: string;
    values: CurrencyValue[];
}