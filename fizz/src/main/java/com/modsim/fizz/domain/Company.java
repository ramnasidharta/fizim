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
    private LocalDate categoryStartDate;
    private String issuerSituation;
    private LocalDate issuerSituationStartDate;
    private String addrType;
    private String publicSpace;
    private String addrComplement;
    private String neighborhood;
    private String county;
    private String st;
    private String country;
    private String zip;
    private String std;
    private String phone;
    private String email;
    private String respType;
    private String respName;
    private String respActingStartDate;
    private String respPublicSpace;
    private String respAddrComplement;
    private String respNeighbourhood;
    private String respCounty;
    private String respSt;
    private String respCountry;
    private String respZip;
    private String respStd;
    private String respPhone;
    private String respEmail;
    private String cnpjAuditor;
    private String auditor;
}
