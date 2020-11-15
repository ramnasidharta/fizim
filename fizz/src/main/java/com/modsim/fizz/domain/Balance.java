package com.modsim.fizz.domain;

import java.io.Serializable;
import java.time.LocalDate;
import javax.persistence.*;
import org.hibernate.annotations.Cache;
import org.hibernate.annotations.CacheConcurrencyStrategy;

/**
 * A Balance.
 */
@Entity
@Table(name = "balance")
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class Balance implements Serializable {
    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "sequenceGenerator")
    @SequenceGenerator(name = "sequenceGenerator")
    private Long id;

    @Column(name = "cnpj")
    private String cnpj;

    @Column(name = "name")
    private String name;

    @Column(name = "cvm_code")
    private Integer cvmCode;

    @Column(name = "category")
    private String category;

    @Column(name = "subcategory")
    private String subcategory;

    @Column(name = "financial_statement")
    private String financialStatement;

    @Column(name = "final_accounting_date")
    private LocalDate finalAccountingDate;

    @Column(name = "value")
    private Double value;

    // jhipster-needle-entity-add-field - JHipster will add fields here
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCnpj() {
        return cnpj;
    }

    public Balance cnpj(String cnpj) {
        this.cnpj = cnpj;
        return this;
    }

    public void setCnpj(String cnpj) {
        this.cnpj = cnpj;
    }

    public String getName() {
        return name;
    }

    public Balance name(String name) {
        this.name = name;
        return this;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getCvmCode() {
        return cvmCode;
    }

    public Balance cvmCode(Integer cvmCode) {
        this.cvmCode = cvmCode;
        return this;
    }

    public void setCvmCode(Integer cvmCode) {
        this.cvmCode = cvmCode;
    }

    public String getCategory() {
        return category;
    }

    public Balance category(String category) {
        this.category = category;
        return this;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getSubcategory() {
        return subcategory;
    }

    public Balance subcategory(String subcategory) {
        this.subcategory = subcategory;
        return this;
    }

    public void setSubcategory(String subcategory) {
        this.subcategory = subcategory;
    }

    public String getFinancialStatement() {
        return financialStatement;
    }

    public Balance financialStatement(String financialStatement) {
        this.financialStatement = financialStatement;
        return this;
    }

    public void setFinancialStatement(String financialStatement) {
        this.financialStatement = financialStatement;
    }

    public LocalDate getFinalAccountingDate() {
        return finalAccountingDate;
    }

    public Balance finalAccountingDate(LocalDate finalAccountingDate) {
        this.finalAccountingDate = finalAccountingDate;
        return this;
    }

    public void setFinalAccountingDate(LocalDate finalAccountingDate) {
        this.finalAccountingDate = finalAccountingDate;
    }

    public Double getValue() {
        return value;
    }

    public Balance value(Double value) {
        this.value = value;
        return this;
    }

    public void setValue(Double value) {
        this.value = value;
    }

    // jhipster-needle-entity-add-getters-setters - JHipster will add getters and setters here

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof Balance)) {
            return false;
        }
        return id != null && id.equals(((Balance) o).id);
    }

    @Override
    public int hashCode() {
        return 31;
    }

    // prettier-ignore
    @Override
    public String toString() {
        return "Balance{" +
            "id=" + getId() +
            ", cnpj='" + getCnpj() + "'" +
            ", name='" + getName() + "'" +
            ", cvmCode=" + getCvmCode() +
            ", category='" + getCategory() + "'" +
            ", subcategory='" + getSubcategory() + "'" +
            ", financialStatement='" + getFinancialStatement() + "'" +
            ", finalAccountingDate='" + getFinalAccountingDate() + "'" +
            ", value=" + getValue() +
            "}";
    }
}
