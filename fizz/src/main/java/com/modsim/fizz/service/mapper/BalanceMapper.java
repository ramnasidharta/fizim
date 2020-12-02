package com.modsim.fizz.service.mapper;

import com.modsim.fizz.domain.*;
import com.modsim.fizz.service.dto.BalanceDTO;
import org.mapstruct.*;

/**
 * Mapper for the entity {@link Balance} and its DTO {@link BalanceDTO}.
 */
@Mapper(componentModel = "spring", uses = {})
public interface BalanceMapper extends EntityMapper<BalanceDTO, Balance> {
    default Balance fromId(Long id) {
        if (id == null) {
            return null;
        }
        Balance balance = new Balance();
        balance.setId(id);
        return balance;
    }
}
