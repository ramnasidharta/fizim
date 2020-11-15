package com.modsim.fizz.service.dto;

import java.io.Serializable;
import java.time.LocalDate;

/**
 * A DTO for the {@link com.modsim.fizz.domain.Balance} entity.
 */
public class BalanceDTO implements Serializable {
    private Long id;

    private String cnpj;

    private String name;

    private Integer cvmCode;

    private String category;

    private String subcategory;

    private String financialStatement;

    private LocalDate finalAccountingDate;

    private Double value;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCnpj() {
        return cnpj;
    }

    public void setCnpj(String cnpj) {
        this.cnpj = cnpj;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getCvmCode() {
        return cvmCode;
    }

    public void setCvmCode(Integer cvmCode) {
        this.cvmCode = cvmCode;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getSubcategory() {
        return subcategory;
    }

    public void setSubcategory(String subcategory) {
        this.subcategory = subcategory;
    }

    public String getFinancialStatement() {
        return financialStatement;
    }

    public void setFinancialStatement(String financialStatement) {
        this.financialStatement = financialStatement;
    }

    public LocalDate getFinalAccountingDate() {
        return finalAccountingDate;
    }

    public void setFinalAccountingDate(LocalDate finalAccountingDate) {
        this.finalAccountingDate = finalAccountingDate;
    }

    public Double getValue() {
        return value;
    }

    public void setValue(Double value) {
        this.value = value;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof BalanceDTO)) {
            return false;
        }

        return id != null && id.equals(((BalanceDTO) o).id);
    }

    @Override
    public int hashCode() {
        return 31;
    }

    // prettier-ignore
    @Override
    public String toString() {
        return "BalanceDTO{" +
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
