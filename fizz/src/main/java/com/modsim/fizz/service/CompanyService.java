package com.modsim.fizz.service;

import com.modsim.fizz.domain.Company;
import com.modsim.fizz.repository.CompanyRepository;
import com.modsim.fizz.service.dto.CompanyDTO;
import com.modsim.fizz.service.mapper.CompanyMapper;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@Transactional
@Slf4j
public class CompanyService {
    private final CompanyRepository repository;
    private final CompanyMapper companyMapper;

    public CompanyService(CompanyRepository repository, CompanyMapper mapper) {
        this.repository = repository;
        this.companyMapper = mapper;
    }

    public CompanyDTO save(CompanyDTO companyDTO) {
        log.debug("Request to save Balance : {}", companyDTO);
        Company company = companyMapper.toEntity(companyDTO);
        company = repository.save(company);
        return companyMapper.toDto(company);
    }

    @Transactional(readOnly = true)
    public Page<CompanyDTO> findAll(Pageable pageable) {
        log.debug("Request to get all Companies");
        return repository.findAll(pageable).map(companyMapper::toDto);
    }

    @Transactional(readOnly = true)
    public Optional<CompanyDTO> findOne(Integer id) {
        log.debug("Request to get Company : {}", id);
        return repository.findById(id).map(companyMapper::toDto);
    }

    public void delete(Integer id) {
        log.debug("Request to delete Company : {}", id);
        repository.deleteById(id);
    }
}
