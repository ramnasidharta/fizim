package com.modsim.fizz.repository;

import com.modsim.fizz.domain.Balance;
import org.springframework.data.jpa.repository.*;
import org.springframework.stereotype.Repository;

/**
 * Spring Data  repository for the Balance entity.
 */
@SuppressWarnings("unused")
@Repository
public interface BalanceRepository extends JpaRepository<Balance, Long> {}
