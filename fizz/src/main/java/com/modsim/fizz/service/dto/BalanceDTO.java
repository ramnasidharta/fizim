package com.modsim.fizz.service.dto;

import com.modsim.fizz.domain.Balance;
import com.modsim.fizz.domain.Company;
import java.io.Serializable;
import java.time.LocalDate;
import lombok.Data;
import org.springframework.beans.BeanUtils;

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

    public Balance toEntity() {
        Balance entity = new Balance();
        BeanUtils.copyProperties(this, entity);
        return entity;
    }

    public static BalanceDTO fromEntity(Balance entity) {
        BalanceDTO dto = new BalanceDTO();
        BeanUtils.copyProperties(entity, dto);
        return dto;
    }
}
