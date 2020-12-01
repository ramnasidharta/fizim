package com.modsim.fizz.service;

import org.springframework.stereotype.Service;

/**
 * This class is responsible for calculating fundamental indicators for CVM companies. Given the CVM code of a company,
 * it gets companies accounting data from the services {@link BalanceService} and {@link CompanyService} and then does
 * the arithmetics of the financial indicator and returns it.
 */
@Service
public class FundamentalIndicatorsService {
    private final BalanceService balanceService;
    private final CompanyService companyService;

    public FundamentalIndicatorsService(BalanceService balanceService, CompanyService companyService) {
        this.balanceService = balanceService;
        this.companyService = companyService;
    }

    public Double priceToEarningRatio(Integer companyCvmCode) {
        return (double) -1;
    }

    public Double debtEquityRatio(Integer companyCvmCode) {
        return (double) -1;
    }

    public Double netCashFlow(Integer companyCvmCode) {
        return (double) -1;
    }

    public Double returnOnEquity(Integer companyCvmCode) {
        return (double) -1;
    }
}
