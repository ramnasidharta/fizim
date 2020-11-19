package com.modsim.fizz.service.dto;

import java.io.Serializable;
import java.time.LocalDate;
import lombok.Data;

/**
 * A DTO for the {@link com.modsim.fizz.domain.Balance} entity.
 */
@Data
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
}
