package com.modsim.fizz.domain;

import java.time.LocalDate;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import lombok.Data;
import org.hibernate.annotations.Cache;
import org.hibernate.annotations.CacheConcurrencyStrategy;

@Entity
@Table(name = "company")
@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
@Data
public class Company {
    @Id
    private Integer cvmCode;

    private String cnpj;
    private String social_denomination;
    private String commercial_denomination;
    private LocalDate register_date;
    private LocalDate constitution_date;
    private LocalDate cancellation_date;
    private String cancellation_reason;
    private String situation;
    private LocalDate situation_start_date;
    private String sector;
    private String market;
    private String category;
    private LocalDate category_start_date;
    private String issuer_situation;
    private LocalDate issuer_situation_start_date;
    private String addr_type;
    private String public_space;
    private String addr_complement;
    private String neighborhood;
    private String county;
    private String st;
    private String country;
    private String zip;
    private String std;
    private String phone;
    private String email;
    private String resp_type;
    private String resp_name;
    private String resp_acting_start_date;
    private String resp_public_space;
    private String resp_addr_complement;
    private String resp_neighbourhood;
    private String resp_county;
    private String resp_st;
    private String resp_country;
    private String resp_zip;
    private String resp_std;
    private String resp_phone;
    private String resp_email;
    private String cnpj_auditor;
    private String auditor;
}
