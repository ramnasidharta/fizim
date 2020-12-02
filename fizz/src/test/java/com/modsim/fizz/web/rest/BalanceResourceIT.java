package com.modsim.fizz.web.rest;

import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.Matchers.hasItem;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.modsim.fizz.FizzApp;
import com.modsim.fizz.domain.Balance;
import com.modsim.fizz.repository.BalanceRepository;
import com.modsim.fizz.service.BalanceService;
import com.modsim.fizz.service.dto.BalanceDTO;
import com.modsim.fizz.service.mapper.BalanceMapper;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.List;
import javax.persistence.EntityManager;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

/**
 * Integration tests for the {@link BalanceResource} REST controller.
 */
@SpringBootTest(classes = FizzApp.class)
@AutoConfigureMockMvc
@WithMockUser
public class BalanceResourceIT {
    private static final String DEFAULT_CNPJ = "AAAAAAAAAA";
    private static final String UPDATED_CNPJ = "BBBBBBBBBB";

    private static final String DEFAULT_NAME = "AAAAAAAAAA";
    private static final String UPDATED_NAME = "BBBBBBBBBB";

    private static final Integer DEFAULT_CVM_CODE = 1;
    private static final Integer UPDATED_CVM_CODE = 2;

    private static final String DEFAULT_CATEGORY = "AAAAAAAAAA";
    private static final String UPDATED_CATEGORY = "BBBBBBBBBB";

    private static final String DEFAULT_SUBCATEGORY = "AAAAAAAAAA";
    private static final String UPDATED_SUBCATEGORY = "BBBBBBBBBB";

    private static final String DEFAULT_FINANCIAL_STATEMENT = "AAAAAAAAAA";
    private static final String UPDATED_FINANCIAL_STATEMENT = "BBBBBBBBBB";

    private static final LocalDate DEFAULT_FINAL_ACCOUNTING_DATE = LocalDate.ofEpochDay(0L);
    private static final LocalDate UPDATED_FINAL_ACCOUNTING_DATE = LocalDate.now(ZoneId.systemDefault());

    private static final Double DEFAULT_VALUE = 1D;
    private static final Double UPDATED_VALUE = 2D;

    @Autowired
    private BalanceRepository balanceRepository;

    @Autowired
    private BalanceMapper balanceMapper;

    @Autowired
    private BalanceService balanceService;

    @Autowired
    private EntityManager em;

    @Autowired
    private MockMvc restBalanceMockMvc;

    private Balance balance;

    /**
     * Create an entity for this test.
     *
     * This is a static method, as tests for other entities might also need it,
     * if they test an entity which requires the current entity.
     */
    public static Balance createEntity(EntityManager em) {
        Balance balance = new Balance()
            .cnpj(DEFAULT_CNPJ)
            .name(DEFAULT_NAME)
            .cvmCode(DEFAULT_CVM_CODE)
            .category(DEFAULT_CATEGORY)
            .subcategory(DEFAULT_SUBCATEGORY)
            .financialStatement(DEFAULT_FINANCIAL_STATEMENT)
            .finalAccountingDate(DEFAULT_FINAL_ACCOUNTING_DATE)
            .value(DEFAULT_VALUE);
        return balance;
    }

    /**
     * Create an updated entity for this test.
     *
     * This is a static method, as tests for other entities might also need it,
     * if they test an entity which requires the current entity.
     */
    public static Balance createUpdatedEntity(EntityManager em) {
        Balance balance = new Balance()
            .cnpj(UPDATED_CNPJ)
            .name(UPDATED_NAME)
            .cvmCode(UPDATED_CVM_CODE)
            .category(UPDATED_CATEGORY)
            .subcategory(UPDATED_SUBCATEGORY)
            .financialStatement(UPDATED_FINANCIAL_STATEMENT)
            .finalAccountingDate(UPDATED_FINAL_ACCOUNTING_DATE)
            .value(UPDATED_VALUE);
        return balance;
    }

    @BeforeEach
    public void initTest() {
        balance = createEntity(em);
    }

    @Test
    @Transactional
    public void getAllBalances() throws Exception {
        // Initialize the database
        balanceRepository.saveAndFlush(balance);

        // Get all the balanceList
        restBalanceMockMvc
            .perform(get("/api/balances?sort=id,desc"))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON_VALUE))
            .andExpect(jsonPath("$.[*].id").value(hasItem(balance.getId().intValue())))
            .andExpect(jsonPath("$.[*].cnpj").value(hasItem(DEFAULT_CNPJ)))
            .andExpect(jsonPath("$.[*].name").value(hasItem(DEFAULT_NAME)))
            .andExpect(jsonPath("$.[*].cvmCode").value(hasItem(DEFAULT_CVM_CODE)))
            .andExpect(jsonPath("$.[*].category").value(hasItem(DEFAULT_CATEGORY)))
            .andExpect(jsonPath("$.[*].subcategory").value(hasItem(DEFAULT_SUBCATEGORY)))
            .andExpect(jsonPath("$.[*].financialStatement").value(hasItem(DEFAULT_FINANCIAL_STATEMENT)))
            .andExpect(jsonPath("$.[*].finalAccountingDate").value(hasItem(DEFAULT_FINAL_ACCOUNTING_DATE.toString())))
            .andExpect(jsonPath("$.[*].value").value(hasItem(DEFAULT_VALUE.doubleValue())));
    }

    @Test
    @Transactional
    public void getBalance() throws Exception {
        // Initialize the database
        balanceRepository.saveAndFlush(balance);

        // Get the balance
        restBalanceMockMvc
            .perform(get("/api/balances/{id}", balance.getId()))
            .andExpect(status().isOk())
            .andExpect(content().contentType(MediaType.APPLICATION_JSON_VALUE))
            .andExpect(jsonPath("$.id").value(balance.getId().intValue()))
            .andExpect(jsonPath("$.cnpj").value(DEFAULT_CNPJ))
            .andExpect(jsonPath("$.name").value(DEFAULT_NAME))
            .andExpect(jsonPath("$.cvmCode").value(DEFAULT_CVM_CODE))
            .andExpect(jsonPath("$.category").value(DEFAULT_CATEGORY))
            .andExpect(jsonPath("$.subcategory").value(DEFAULT_SUBCATEGORY))
            .andExpect(jsonPath("$.financialStatement").value(DEFAULT_FINANCIAL_STATEMENT))
            .andExpect(jsonPath("$.finalAccountingDate").value(DEFAULT_FINAL_ACCOUNTING_DATE.toString()))
            .andExpect(jsonPath("$.value").value(DEFAULT_VALUE.doubleValue()));
    }

    @Test
    @Transactional
    public void getNonExistingBalance() throws Exception {
        // Get the balance
        restBalanceMockMvc.perform(get("/api/balances/{id}", Long.MAX_VALUE)).andExpect(status().isNotFound());
    }
}
