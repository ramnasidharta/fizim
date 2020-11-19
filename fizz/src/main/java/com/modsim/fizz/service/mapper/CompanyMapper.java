package com.modsim.fizz.service.mapper;

import com.modsim.fizz.domain.Company;
import com.modsim.fizz.service.dto.CompanyDTO;
import org.mapstruct.Mapper;

/**
 * Mapper for the entity {@link Company} and its DTO {@link CompanyDTO}.
 */
@Mapper(componentModel = "spring")
public interface CompanyMapper extends EntityMapper<CompanyDTO, Company> {
    default Company fromId(Integer id) {
        if (id == null) {
            return null;
        }
        Company company = new Company();
        company.setCvmCode(id);
        return company;
    }
}
