package com.modsim.fizz.service;

import com.modsim.fizz.domain.Balance;
import com.modsim.fizz.domain.Company;
import com.modsim.fizz.repository.BalanceRepository;
import com.modsim.fizz.service.dto.BalanceDTO;
import com.modsim.fizz.service.mapper.BalanceMapper;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Example;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Service for managing {@link com.modsim.fizz.domain.Balance}.
 */
@Service
@Transactional
@Slf4j
public class BalanceService {
    private final BalanceRepository balanceRepository;

    public BalanceService(BalanceRepository balanceRepository) {
        this.balanceRepository = balanceRepository;
    }

    public BalanceDTO save(BalanceDTO balanceDTO) {
        log.debug("Request to save Balance : {}", balanceDTO);
        Balance balance = balanceDTO.toEntity();
        balance = balanceRepository.save(balance);
        return BalanceDTO.fromEntity(balance);
    }

    @Transactional(readOnly = true)
    public Page<BalanceDTO> findAll(Pageable pageable) {
        log.debug("Request to get all Balances");
        return balanceRepository.findAll(pageable).map(BalanceDTO::fromEntity);
    }

    @Transactional(readOnly = true)
    public Page<BalanceDTO> findAllWithExample(BalanceDTO balanceExample, Pageable pageable) {
        log.debug("Request to get all Balances");
        Example<Balance> entityExample = Example.of(balanceExample.toEntity());
        return balanceRepository.findAll(entityExample, pageable).map(BalanceDTO::fromEntity);
    }

    @Transactional(readOnly = true)
    public Optional<BalanceDTO> findOne(Long id) {
        log.debug("Request to get Balance : {}", id);
        return balanceRepository.findById(id).map(BalanceDTO::fromEntity);
    }

    public void delete(Long id) {
        log.debug("Request to delete Balance : {}", id);
        balanceRepository.deleteById(id);
    }
}
