import axios from 'axios';
import { ICrudGetAction, ICrudGetAllAction, ICrudPutAction, ICrudDeleteAction } from 'react-jhipster';

import { cleanEntity } from 'app/shared/util/entity-utils';
import { REQUEST, SUCCESS, FAILURE } from 'app/shared/reducers/action-type.util';

import { IBalance, defaultValue } from 'app/shared/model/balance.model';

export const ACTION_TYPES = {
  FETCH_BALANCE_LIST: 'balance/FETCH_BALANCE_LIST',
  FETCH_BALANCE: 'balance/FETCH_BALANCE',
  RESET: 'balance/RESET',
};

const initialState = {
  loading: false,
  errorMessage: null,
  entities: [] as ReadonlyArray<IBalance>,
  entity: defaultValue,
  updating: false,
  totalItems: 0,
  updateSuccess: false,
};

export type BalanceState = Readonly<typeof initialState>;

// Reducer

export default (state: BalanceState = initialState, action): BalanceState => {
  switch (action.type) {
    case REQUEST(ACTION_TYPES.FETCH_BALANCE_LIST):
    case REQUEST(ACTION_TYPES.FETCH_BALANCE):
      return {
        ...state,
        errorMessage: null,
        updateSuccess: false,
        loading: true,
      };
    case FAILURE(ACTION_TYPES.FETCH_BALANCE_LIST):
    case FAILURE(ACTION_TYPES.FETCH_BALANCE):
      return {
        ...state,
        loading: false,
        updating: false,
        updateSuccess: false,
        errorMessage: action.payload,
      };
    case SUCCESS(ACTION_TYPES.FETCH_BALANCE_LIST):
      return {
        ...state,
        loading: false,
        entities: action.payload.data,
        totalItems: parseInt(action.payload.headers['x-total-count'], 10),
      };
    case SUCCESS(ACTION_TYPES.FETCH_BALANCE):
      return {
        ...state,
        loading: false,
        entity: action.payload.data,
      };
    case ACTION_TYPES.RESET:
      return {
        ...initialState,
      };
    default:
      return state;
  }
};

const apiUrl = 'api/balances';

// Actions

export const getEntities: ICrudGetAllAction<IBalance> = (page, size, sort) => {
  const requestUrl = `${apiUrl}${sort ? `?page=${page}&size=${size}&sort=${sort}` : ''}`;
  return {
    type: ACTION_TYPES.FETCH_BALANCE_LIST,
    payload: axios.get<IBalance>(`${requestUrl}${sort ? '&' : '?'}cacheBuster=${new Date().getTime()}`),
  };
};

export const getEntity: ICrudGetAction<IBalance> = id => {
  const requestUrl = `${apiUrl}/${id}`;
  return {
    type: ACTION_TYPES.FETCH_BALANCE,
    payload: axios.get<IBalance>(requestUrl),
  };
};

export const reset = () => ({
  type: ACTION_TYPES.RESET,
});
