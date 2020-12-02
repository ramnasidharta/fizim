package com.modsim.fizz.web.rest;

import com.modsim.fizz.service.BalanceService;
import com.modsim.fizz.service.dto.BalanceDTO;
import com.modsim.fizz.web.rest.errors.BadRequestAlertException;
import io.github.jhipster.web.util.HeaderUtil;
import io.github.jhipster.web.util.PaginationUtil;
import io.github.jhipster.web.util.ResponseUtil;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

/**
 * REST controller for managing {@link com.modsim.fizz.domain.Balance}.
 */
@RestController
@RequestMapping("/api/balances")
public class BalanceResource {
    private final Logger log = LoggerFactory.getLogger(BalanceResource.class);

    private final BalanceService balanceService;

    public BalanceResource(BalanceService balanceService) {
        this.balanceService = balanceService;
    }

    /**
     * {@code GET  /balances} : get all the balances.
     *
     * @param pageable the pagination information.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and the list of balances in body.
     */
    @GetMapping
    public ResponseEntity<List<BalanceDTO>> getAllBalances(BalanceDTO balanceDTO, Pageable pageable) {
        log.debug("REST request GET /balances with body {} and pagination {}", balanceDTO, pageable);
        Page<BalanceDTO> page = balanceService.findAllWithExample(balanceDTO, pageable);
        HttpHeaders headers = PaginationUtil.generatePaginationHttpHeaders(ServletUriComponentsBuilder.fromCurrentRequest(), page);
        return ResponseEntity.ok().headers(headers).body(page.getContent());
    }

    /**
     * {@code GET  /balances/:id} : get the "id" balance.
     *
     * @param id the id of the balanceDTO to retrieve.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the balanceDTO, or with status {@code 404 (Not Found)}.
     */
    @GetMapping("/{id}")
    public ResponseEntity<BalanceDTO> getBalance(@PathVariable Long id) {
        log.debug("REST request to get Balance : {}", id);
        Optional<BalanceDTO> balanceDTO = balanceService.findOne(id);
        return ResponseUtil.wrapOrNotFound(balanceDTO);
    }
}
