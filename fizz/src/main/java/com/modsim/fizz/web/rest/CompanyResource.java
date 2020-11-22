package com.modsim.fizz.web.rest;

import com.modsim.fizz.service.CompanyService;
import com.modsim.fizz.service.dto.CompanyDTO;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Example;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("api/companies/")
@Slf4j
public class CompanyResource {
    private CompanyService service;

    public CompanyResource(CompanyService service) {
        this.service = service;
    }

    @GetMapping
    public ResponseEntity<Page<CompanyDTO>> findAll(@RequestBody CompanyDTO companyDTO, Pageable pageable) {
        log.info("REST request GET /companies with body {} and pagination {}", companyDTO, pageable);
        Page<CompanyDTO> result = service.findAllWithExample(companyDTO, pageable);
        return ResponseEntity.ok(result);
    }
}
