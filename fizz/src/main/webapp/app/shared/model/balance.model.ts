import { Moment } from 'moment';

export interface IBalance {
  id?: number;
  cnpj?: string;
  name?: string;
  cvmCode?: number;
  category?: string;
  subcategory?: string;
  financialStatement?: string;
  finalAccountingDate?: string;
  value?: number;
}

export const defaultValue: Readonly<IBalance> = {};
