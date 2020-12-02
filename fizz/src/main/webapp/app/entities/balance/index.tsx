import React from 'react';
import { Switch } from 'react-router-dom';

import ErrorBoundaryRoute from 'app/shared/error/error-boundary-route';

import Balance from './balance';
import BalanceDetail from './balance-detail';

const Routes = ({ match }) => (
  <>
    <Switch>
      <ErrorBoundaryRoute exact path={`${match.url}/:id`} component={BalanceDetail} />
      <ErrorBoundaryRoute path={match.url} component={Balance} />
    </Switch>
  </>
);

export default Routes;
