import React, { useState, useEffect } from 'react';
import { connect } from 'react-redux';
import { Link, RouteComponentProps } from 'react-router-dom';
import { Button, Col, Row, Table } from 'reactstrap';
import { Translate, ICrudGetAllAction, TextFormat, getSortState, IPaginationBaseState, JhiPagination, JhiItemCount } from 'react-jhipster';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { IRootState } from 'app/shared/reducers';
import { getEntities } from './balance.reducer';
import { IBalance } from 'app/shared/model/balance.model';
import { APP_DATE_FORMAT, APP_LOCAL_DATE_FORMAT } from 'app/config/constants';
import { ITEMS_PER_PAGE } from 'app/shared/util/pagination.constants';
import { overridePaginationStateWithQueryParams } from 'app/shared/util/entity-utils';

export interface IBalanceProps extends StateProps, DispatchProps, RouteComponentProps<{ url: string }> {}

export const Balance = (props: IBalanceProps) => {
  const [paginationState, setPaginationState] = useState(
    overridePaginationStateWithQueryParams(getSortState(props.location, ITEMS_PER_PAGE), props.location.search)
  );

  const getAllEntities = () => {
    props.getEntities(paginationState.activePage - 1, paginationState.itemsPerPage, `${paginationState.sort},${paginationState.order}`);
  };

  const sortEntities = () => {
    getAllEntities();
    const endURL = `?page=${paginationState.activePage}&sort=${paginationState.sort},${paginationState.order}`;
    if (props.location.search !== endURL) {
      props.history.push(`${props.location.pathname}${endURL}`);
    }
  };

  useEffect(() => {
    sortEntities();
  }, [paginationState.activePage, paginationState.order, paginationState.sort]);

  useEffect(() => {
    const params = new URLSearchParams(props.location.search);
    const page = params.get('page');
    const sort = params.get('sort');
    if (page && sort) {
      const sortSplit = sort.split(',');
      setPaginationState({
        ...paginationState,
        activePage: +page,
        sort: sortSplit[0],
        order: sortSplit[1],
      });
    }
  }, [props.location.search]);

  const sort = p => () => {
    setPaginationState({
      ...paginationState,
      order: paginationState.order === 'asc' ? 'desc' : 'asc',
      sort: p,
    });
  };

  const handlePagination = currentPage =>
    setPaginationState({
      ...paginationState,
      activePage: currentPage,
    });

  const { balanceList, match, loading, totalItems } = props;
  return (
    <div>
      <h2 id="balance-heading">
        <Translate contentKey="fizzApp.balance.home.title">Balances</Translate>
      </h2>
      <div className="table-responsive">
        {balanceList && balanceList.length > 0 ? (
          <Table responsive>
            <thead>
              <tr>
                <th className="hand" onClick={sort('id')}>
                  <Translate contentKey="global.field.id">ID</Translate> <FontAwesomeIcon icon="sort" />
                </th>
                <th className="hand" onClick={sort('cnpj')}>
                  <Translate contentKey="fizzApp.balance.cnpj">Cnpj</Translate> <FontAwesomeIcon icon="sort" />
                </th>
                <th className="hand" onClick={sort('name')}>
                  <Translate contentKey="fizzApp.balance.name">Name</Translate> <FontAwesomeIcon icon="sort" />
                </th>
                <th className="hand" onClick={sort('cvmCode')}>
                  <Translate contentKey="fizzApp.balance.cvmCode">Cvm Code</Translate> <FontAwesomeIcon icon="sort" />
                </th>
                <th className="hand" onClick={sort('category')}>
                  <Translate contentKey="fizzApp.balance.category">Category</Translate> <FontAwesomeIcon icon="sort" />
                </th>
                <th className="hand" onClick={sort('subcategory')}>
                  <Translate contentKey="fizzApp.balance.subcategory">Subcategory</Translate> <FontAwesomeIcon icon="sort" />
                </th>
                <th className="hand" onClick={sort('financialStatement')}>
                  <Translate contentKey="fizzApp.balance.financialStatement">Financial Statement</Translate> <FontAwesomeIcon icon="sort" />
                </th>
                <th className="hand" onClick={sort('finalAccountingDate')}>
                  <Translate contentKey="fizzApp.balance.finalAccountingDate">Final Accounting Date</Translate>{' '}
                  <FontAwesomeIcon icon="sort" />
                </th>
                <th className="hand" onClick={sort('value')}>
                  <Translate contentKey="fizzApp.balance.value">Value</Translate> <FontAwesomeIcon icon="sort" />
                </th>
                <th />
              </tr>
            </thead>
            <tbody>
              {balanceList.map((balance, i) => (
                <tr key={`entity-${i}`}>
                  <td>
                    <Button tag={Link} to={`${match.url}/${balance.id}`} color="link" size="sm">
                      {balance.id}
                    </Button>
                  </td>
                  <td>{balance.cnpj}</td>
                  <td>{balance.name}</td>
                  <td>{balance.cvmCode}</td>
                  <td>{balance.category}</td>
                  <td>{balance.subcategory}</td>
                  <td>{balance.financialStatement}</td>
                  <td>
                    {balance.finalAccountingDate ? (
                      <TextFormat type="date" value={balance.finalAccountingDate} format={APP_LOCAL_DATE_FORMAT} />
                    ) : null}
                  </td>
                  <td>{balance.value}</td>
                  <td className="text-right">
                    <div className="btn-group flex-btn-group-container">
                      <Button tag={Link} to={`${match.url}/${balance.id}`} color="info" size="sm">
                        <FontAwesomeIcon icon="eye" />{' '}
                        <span className="d-none d-md-inline">
                          <Translate contentKey="entity.action.view">View</Translate>
                        </span>
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        ) : (
          !loading && (
            <div className="alert alert-warning">
              <Translate contentKey="fizzApp.balance.home.notFound">No Balances found</Translate>
            </div>
          )
        )}
      </div>
      {props.totalItems ? (
        <div className={balanceList && balanceList.length > 0 ? '' : 'd-none'}>
          <Row className="justify-content-center">
            <JhiItemCount page={paginationState.activePage} total={totalItems} itemsPerPage={paginationState.itemsPerPage} i18nEnabled />
          </Row>
          <Row className="justify-content-center">
            <JhiPagination
              activePage={paginationState.activePage}
              onSelect={handlePagination}
              maxButtons={5}
              itemsPerPage={paginationState.itemsPerPage}
              totalItems={props.totalItems}
            />
          </Row>
        </div>
      ) : (
        ''
      )}
    </div>
  );
};

const mapStateToProps = ({ balance }: IRootState) => ({
  balanceList: balance.entities,
  loading: balance.loading,
  totalItems: balance.totalItems,
});

const mapDispatchToProps = {
  getEntities,
};

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(mapStateToProps, mapDispatchToProps)(Balance);
