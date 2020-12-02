import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import { Link, RouteComponentProps } from 'react-router-dom';
import { Button, Row, Col } from 'reactstrap';
import { Translate, ICrudGetAction, TextFormat } from 'react-jhipster';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { IRootState } from 'app/shared/reducers';
import { getEntity } from './balance.reducer';
import { IBalance } from 'app/shared/model/balance.model';
import { APP_DATE_FORMAT, APP_LOCAL_DATE_FORMAT } from 'app/config/constants';

export interface IBalanceDetailProps extends StateProps, DispatchProps, RouteComponentProps<{ id: string }> {}

export const BalanceDetail = (props: IBalanceDetailProps) => {
  useEffect(() => {
    props.getEntity(props.match.params.id);
  }, []);

  const { balanceEntity } = props;
  return (
    <Row>
      <Col md="8">
        <h2>
          <Translate contentKey="fizzApp.balance.detail.title">Balance</Translate> [<b>{balanceEntity.id}</b>]
        </h2>
        <dl className="jh-entity-details">
          <dt>
            <span id="cnpj">
              <Translate contentKey="fizzApp.balance.cnpj">Cnpj</Translate>
            </span>
          </dt>
          <dd>{balanceEntity.cnpj}</dd>
          <dt>
            <span id="name">
              <Translate contentKey="fizzApp.balance.name">Name</Translate>
            </span>
          </dt>
          <dd>{balanceEntity.name}</dd>
          <dt>
            <span id="cvmCode">
              <Translate contentKey="fizzApp.balance.cvmCode">Cvm Code</Translate>
            </span>
          </dt>
          <dd>{balanceEntity.cvmCode}</dd>
          <dt>
            <span id="category">
              <Translate contentKey="fizzApp.balance.category">Category</Translate>
            </span>
          </dt>
          <dd>{balanceEntity.category}</dd>
          <dt>
            <span id="subcategory">
              <Translate contentKey="fizzApp.balance.subcategory">Subcategory</Translate>
            </span>
          </dt>
          <dd>{balanceEntity.subcategory}</dd>
          <dt>
            <span id="financialStatement">
              <Translate contentKey="fizzApp.balance.financialStatement">Financial Statement</Translate>
            </span>
          </dt>
          <dd>{balanceEntity.financialStatement}</dd>
          <dt>
            <span id="finalAccountingDate">
              <Translate contentKey="fizzApp.balance.finalAccountingDate">Final Accounting Date</Translate>
            </span>
          </dt>
          <dd>
            {balanceEntity.finalAccountingDate ? (
              <TextFormat value={balanceEntity.finalAccountingDate} type="date" format={APP_LOCAL_DATE_FORMAT} />
            ) : null}
          </dd>
          <dt>
            <span id="value">
              <Translate contentKey="fizzApp.balance.value">Value</Translate>
            </span>
          </dt>
          <dd>{balanceEntity.value}</dd>
        </dl>
        <Button tag={Link} to="/balance" replace color="info">
          <FontAwesomeIcon icon="arrow-left" />{' '}
          <span className="d-none d-md-inline">
            <Translate contentKey="entity.action.back">Back</Translate>
          </span>
        </Button>
        &nbsp;
        <Button tag={Link} to={`/balance/${balanceEntity.id}/edit`} replace color="primary">
          <FontAwesomeIcon icon="pencil-alt" />{' '}
          <span className="d-none d-md-inline">
            <Translate contentKey="entity.action.edit">Edit</Translate>
          </span>
        </Button>
      </Col>
    </Row>
  );
};

const mapStateToProps = ({ balance }: IRootState) => ({
  balanceEntity: balance.entity,
});

const mapDispatchToProps = { getEntity };

type StateProps = ReturnType<typeof mapStateToProps>;
type DispatchProps = typeof mapDispatchToProps;

export default connect(mapStateToProps, mapDispatchToProps)(BalanceDetail);
