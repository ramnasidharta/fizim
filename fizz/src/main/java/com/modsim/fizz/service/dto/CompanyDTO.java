package com.modsim.fizz.service.dto;

import java.time.LocalDate;
import lombok.Data;

/**
 * A DTO for the {@link com.modsim.fizz.domain.Company} entity.
 */
@Data
public class CompanyDTO {
    private Integer cvmCode;
    private String cnpj;
    private String social_denomination;
    private String comercial_denomination;
    private LocalDate register_date;
    private LocalDate constitution_date;
    private LocalDate cancellation_date;
    private String cancellation_reason;
    private String situation;
    private LocalDate situation_start_date;
    private String sector;
    private String market;
    private String category;
    private String cnpj_auditor;
    private String auditor;
}
