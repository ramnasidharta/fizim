package com.modsim.fizz.service;

import com.modsim.fizz.domain.Company;
import com.modsim.fizz.repository.CompanyRepository;
import com.modsim.fizz.service.dto.CompanyDTO;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Example;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
@Slf4j
public class CompanyService {
    private final CompanyRepository repository;

    public CompanyService(CompanyRepository repository) {
        this.repository = repository;
    }

    public CompanyDTO save(CompanyDTO companyDTO) {
        log.debug("Request to save Balance : {}", companyDTO);
        Company company = companyDTO.toEntity();
        company = repository.save(company);
        return CompanyDTO.fromEntity(company);
    }

    @Transactional(readOnly = true)
    public Page<CompanyDTO> findAllWithExample(CompanyDTO companyExample, Pageable pageable) {
        log.debug("Request to get all Companies");
        Example<Company> entityExample = Example.of(companyExample.toEntity());
        return repository.findAll(entityExample, pageable).map(CompanyDTO::fromEntity);
    }

    @Transactional(readOnly = true)
    public Optional<CompanyDTO> findOne(Integer id) {
        log.debug("Request to get Company : {}", id);
        return repository.findById(id).map(CompanyDTO::fromEntity);
    }

    public void delete(Integer id) {
        log.debug("Request to delete Company : {}", id);
        repository.deleteById(id);
    }
}
