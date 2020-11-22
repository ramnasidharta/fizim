package com.modsim.fizz.service.dto;

import com.modsim.fizz.domain.Company;
import java.time.LocalDate;
import lombok.Data;
import org.springframework.beans.BeanUtils;

/**
 * A DTO for the {@link com.modsim.fizz.domain.Company} entity.
 */
@Data
public class CompanyDTO {
    private Integer cvmCode;
    private String cnpj;
    private String socialDenomination;
    private String commercialDenomination;
    private LocalDate registerDate;
    private LocalDate constitutionDate;
    private LocalDate cancellationDate;
    private String cancellationReason;
    private String situation;
    private LocalDate situationStartDate;
    private String sector;
    private String market;
    private String category;
    private String cnpjAuditor;
    private String auditor;

    public Company toEntity() {
        Company entity = new Company();
        BeanUtils.copyProperties(this, entity);
        return entity;
    }

    public static CompanyDTO fromEntity(Company entity) {
        CompanyDTO dto = new CompanyDTO();
        BeanUtils.copyProperties(entity, dto);
        return dto;
    }
}
