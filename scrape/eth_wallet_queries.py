INSERT_WALLET_BALANCE = \
    """
    INSERT INTO wallet (address, owner, transaction_count, balance) 
    VALUES (%s, %s, %s, %s) 
    ON DUPLICATE KEY UPDATE transaction_count=%s, balance=%s
    """

INSERT_TOKEN_INFO = \
    """
    INSERT INTO token (address, name, price, symbol) 
    VALUES (%s, %s, %s, %s) 
    ON DUPLICATE KEY UPDATE price=%s
    """

INSERT_WALLET_HOLDINGS = \
    """
    INSERT INTO wallet_holding (wallet_id, token_id, balance) 
    VALUES (%s, %s, %s) 
    ON DUPLICATE KEY UPDATE balance=%s
    """

CREATE_TOKEN_TABLE = \
    """
    CREATE TABLE `token` (
      `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
      `address` varchar(255) NOT NULL DEFAULT '',
      `name` varchar(100) DEFAULT '',
      `price` bigint(20) DEFAULT NULL,
      `symbol` varchar(100) DEFAULT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `address` (`address`)
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
    """


CREATE_WALLET_TABLE = \
    """
    CREATE TABLE `wallet` (
      `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
      `address` varchar(255) NOT NULL DEFAULT '',
      `owner` varchar(100) DEFAULT NULL,
      `transaction_count` int(11) NOT NULL,
      `balance` decimal(65,2) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `address` (`address`)
    ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;
    """

CREATE_WALLET_HOLDING = \
    """
    CREATE TABLE `wallet_holding` (
      `wallet_id` int(11) NOT NULL,
      `token_id` int(11) NOT NULL,
      `balance` decimal(65,2) NOT NULL,
      UNIQUE KEY `wallet_id_2` (`wallet_id`,`token_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """