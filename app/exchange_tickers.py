
def crypto_to_ticker(Crypto):

  cryptos = {'0Chain': 'ZCN','0x': 'ZRX','12Ships': 'TSHP','ARPA Chain': 'ARPA','Aave': 'LEND','Abyss Token': 'ABYSS','AdEx': 'ADX','Aeon': 'AEON',
    'Aeron': 'ARN','Aeternity': 'AE','Agrello': 'DLT','AidCoin': 'AID','Aion': 'AIO','AirSwap': 'AST','Akropolis': 'AKRO','Algorand': 'ALGO',
    'Ambrosus': 'AMB','Ampleforth': 'AMPL','Ankr': 'ANKR','AppCoins': 'APPC','Aragon': 'ANT','Ardor': 'ARDR','Ark': 'ARK','Atonomi': 'ATMI','Auctus': 'AUC',
    'Augur': 'REP','Autonio': 'NIO','Aventus': 'AVT','BANKEX': 'BKX','BLOCKv': 'VEE','BORA': 'BORA','BTU Protocol': 'BTU','Bancor': 'BNT',
    'Band Protocol': 'BAND','Banyan Network': 'BBN','Basic Attention Token': 'BAT','Beam': 'BEAM','Binance Coin': 'BNB','Binance GBP Stable Coin': 'BGBP',
    'Binance USD': 'BUSD','BitKan': 'KAN','BitShares': 'BTS','BitTorrent': 'BTT','BitTube': 'TUBE','Bitcoin': 'BTC','Bitcoin Cash': 'BCH',
    'Bitcoin Diamond': 'BCD','Bitcoin Gold': 'BTG','Bitcoin Interest': 'BCI','Bitcoin SV': 'BSV','BlackCoin': 'BLK','Blockcloud': 'BLOC',
    'Blockmason Credit Protocol': 'BCPT','Blocknet': 'BLOCK','Blockpass': 'PASS','Blockstack': 'STX','Blox': 'CDT','Bluzelle': 'BLZ','BnkToTheFuture': 'BFT',
    'Bread': 'BRD','Burst': 'BURST','Bytom': 'BTM','Callisto Network': 'CLO','Cardano': 'ADA','Celer Network': 'CELR','Chainlink': 'LINK','Chiliz': 'CHZ',
    'Chromia': 'CHR','Cindicator': 'CND','Civic': 'CVC','Cocos-BCX': 'COCOS','CommerceBlock': 'CBT','Content Neutrality Network': 'CNN','ContentBox': 'BOX',
    'Contentos': 'COS','Cortex': 'CTXC','Cosmo Coin': 'COSM','Cosmos': 'ATOM','Cred': 'LBA','Credits': 'CS','Crowd Machine': 'CMCT','Crown': 'CRW',
    'Crypto.com Coin': 'CRO','CryptoFranc': 'XCHF','Curecoin': 'CURE','CyberMiles': 'CMT','DAOstack': 'GEN','DATA': 'DTA','DECENT': 'DCT','DMarket': 'DMT',
    'Dash': 'DASH','Decentraland': 'MANA','Decred': 'DCR','Dent': 'DENT','Dether': 'DTH','DigiByte': 'DGB','DigitalNote': 'XDN','Digix Gold Token': 'DGX',
    'DigixDAO': 'DGD','Dock': 'DOCK','Dogecoin': 'DOGE','Dragon Token': 'DT','Dragonchain': 'DRGN','Dusk Network': 'DUSK','EOS': 'EOS','Edge': 'DADI',
    'Edgeless': 'EDG','Eidoo': 'EDO','Einsteinium': 'EMC2','Elrond': 'ERD','Endor Protocol': 'EDR','Enigma': 'ENG','Enjin Coin': 'ENJ','Essentia': 'ESS',
    'Ether Kingdoms Token': 'IMP','Ethereum': 'ETH','Ethereum Classic': 'ETC','Etherparty': 'FUEL','Everex': 'EVX','Everipedia': 'IQX',
    'ExclusiveCoin': 'EXCL','Expanse': 'EXP','FLETA': 'FLETA','FLO': 'FLO','FNB Protocol': 'FNB','FOAM': 'FOAM','FTX Token': 'FTT','Factom': 'FCT',
    'Fantom': 'FTM','Feathercoin': 'FTC','Fetch.ai': 'FET','FirstBlood': '1ST','Flexacoin': 'FXC','FunFair': 'FUN','Function X': 'FX','Fusion': 'FSN',
    'GXChain': 'GXS','GameCredits': 'GAME','Gas': 'GAS','Gemini Dollar': 'GSD','Genesis Vision': 'GVT','GeoCoin': 'GEO','Gifto': 'GTO','Gnosis': 'GNO',
    'GoChain': 'GO','Golem': 'GNT','Grin': 'GRIN','Groestlcoin': 'GRS','Gulden': 'NLG','Harmony': 'ONE','Haven Protocol': 'XHV','Hdac': 'HDAC',
    'Hedera Hashgraph': 'HBAR','HedgeTrade': 'HEDG','Holo': 'HOT','Horizen': 'ZEN','Humaniq': 'HMQ','Hxro': 'HXRO','Hydro': 'HYDRO','Hydro Protocol': 'HOT',
    'HyperCash': 'HC','I/O Coin': 'IOC','ICON': 'ICX','IHT Real Estate Protocol': 'IHT','INT Chain': 'INT','ION': 'ION','IOST': 'IOST','IOTA': 'IOTA',
    'Ignis': 'IGNIS','Incent': 'INCNT','Insolar': 'INS','IoTeX': 'IOTX','Jibrel Network': 'JNT','Kava': 'KAVA','Kleros': 'PNK','Komodo': 'KMD',
    'Kyber Network': 'KNC','LBRY Credits': 'LBC','LUNA': 'LUNA','Lambda': 'LAMB','Lisk': 'LSK','Litecoin': 'LTC','Loom Network': 'LOOM','Loopring': 'LRC',
    'Lunyr': 'LUN','Lympo': 'LYM','MCO': 'MCO','Maecenas': 'ART','MaidSafeCoin': 'MAID','Mainframe': 'MFT','Maker': 'MKR','Matic Network': 'MATIC',
    'Matrix AI Network': 'MAN','Medicalchain': 'MTN','Melon': 'MLN','Memetic / PepeCoin': 'MEME','Mercury': 'MER','Metadium': 'META','Metal': 'MTL',
    'Metaverse ETP': 'ETP','Metronome': 'MET','Mithril': 'MITH','MobileGo': 'MGO','Moeda Loyalty Points': 'MDA','MonaCoin': 'MONA','Monero': 'XMR',
    'MonetaryUnit': 'MUE','Monetha': 'MTH','Monolith': 'TKN','More Coin': 'MORE','Morpheus.Network': 'MRPH','Multi-collateral DAI': 'DAI','Myriad': 'XMY',
    'NEM': 'XEM','NEO': 'NEO','NKN': 'NKN','NULS': 'NULS','Nano': 'NANO','NavCoin': 'NAV','Neblio': 'NEBL','Nebulas': 'NAS','Nectar': 'NEC','Nexus': 'NXS',
    'NoLimitCoin': 'NLC2','Nucleus Vision': 'NCASH','Numeraire': 'NMR','Nxt': 'NXT','OAX': 'OAX','ODEM': 'ODE','OKB': 'OKB','OKCash': 'OK','ORS Group': 'ORS',
    'OST': 'OST','Obyte': 'GBYTE','Ocean Protocol': 'OCEAN','OmiseGO': 'OMG','Omni': 'OMN','On.Live': 'ONL','Ontology': 'ONT','Ontology Gas': 'ONG',
    'Orbs': 'ORBS','OriginTrail': 'TRAC','PAL Network': 'PAL','PCHAIN': 'PI','PIVX': 'PIVX','PIXEL': 'PXL','POA': 'POA','ParkinGo': 'GOT','Particl': 'PART',
    'Patientory': 'PTOY','Paxos Standard': 'PAX','Peercoin': 'PPC','Perlin': 'PERL','Pinkcoin': 'PINK','PlayChip': 'PLA','Pledge Coin': 'PLG','Po.et': 'POE',
    'Polymath': 'POLY','Populous': 'PPT','PotCoin': 'POT','Power Ledger': 'POWR','Project Pai': 'PAI','Prometeus': 'PROM','PumaPay': 'PMA','Pundi X': 'NPXS',
    'QASH': 'QASH','QLC Chain': 'QLC','Qtum': 'QTUM','Quant': 'QNT','Quantstamp': 'QSP','Quantum Resistant Ledger': 'QRL','QuarkChain': 'QKC',
    'RIF Token': 'RIF','RSK Smart Bitcoin': 'RBT','Radium': 'RADS','Raiden Network Token': 'RDN','Rate3': 'RTE','Ravencoin': 'RVN','Red Pulse Phoenix': 'PHB',
    'ReddCoin': 'RDD','Refereum': 'RFR','Ren': 'REN','Request': 'REQ','Ripio Credit Network': 'RCN','SEER': 'SEER','SIBCoin': 'SIB','SIRIN LABS Token': 'SRN',
    'SIX': 'SIX','SOLVE': 'SOLVE','SONM': 'SNM','STASIS EURO': 'EURS','STPT': 'STPT','SaluS': 'SLS','Santiment Network Token': 'SAN','Selfkey': 'KEY',
    'Sentinel Protocol': 'UPP','Siacoin': 'SC','SingularDTV': 'SNGLS','SingularityNET': 'AGI','Skycoin': 'SKY','SpaceChain': 'SPC','SpankChain': 'SPANK',
    'Spendcoin': 'SPND','Sphere': 'SPHR','StableUSD': 'USDS','Status': 'SNT','Stealth': 'XST','Steem': 'STEEM','Steem Dollars': 'SBD','Stellar': 'XLM',
    'Storj': 'STORJ','Storm': 'STORM','Stratis': 'STRAT','Streamr DATAcoin': 'DATA','Swarm': 'SWM','Syscoin': 'SYS','TEMCO': 'TEMCO','THETA': 'THETA',
    'TRON': 'TRX','TROY': 'TROY','TTC': 'TTC','Tael': 'WABI','TenX': 'PAY','Tether': 'USDT','Tezos': 'XTZ','Theta Fuel': 'TFUEL','Tierion': 'TNT',
    'Time New Bank': 'TNB','TomoChain': 'TOMO','Tripio': 'TRIO','TrueUSD': 'TSD',"Tutor's Diary": 'TUDA','UNUS SED LEO': 'LEO','USD Coin': 'USDC',
    'USDK': 'USDK','Ubiq': 'UBQ','Ultra': 'UOS','Unikoin Gold': 'UKG','Universa': 'UTNP','Upfiring': 'UFR','Uranus': 'URAC','Utrust': 'UTK',
    'V Systems': 'VSY','VIBE': 'VIBE','VITE': 'VITE','VeChain': 'VET','Verge': 'XVG','VeriBlock': 'VBK','VeriCoin': 'VRC','Vertcoin': 'VTC','Vetri': 'VLD',
    'Viacoin': 'VIA','Viberate': 'VIB','Vodi X': 'VDX','Voyager Token': 'BQX','W Green Pay': 'WGP','WAX': 'WAXP','WINk': 'WIN','WOLLO': 'WLO',
    'Waltonchain': 'WTC','Wanchain': 'WAN','Waves': 'WAVES','WePower': 'WPR','Wrapped Bitcoin': 'WBTC','XEL': 'XEL','XRP': 'XRP','Xriba': 'XRA',
    'YGGDRASH': 'YEED','YOYOW': 'YOYO','ZB Token': 'ZBT','Zcash': 'ZEC','Zcoin': 'XZC','Zilliqa': 'ZIL','adToken': 'ADT','aelf': 'ELF','district0x': 'DNT',
    'iExec RLC': 'RLC'}

  for crypto, ticker in cryptos.items():
        if Crypto == crypto:
            return ticker

def stock_to_ticker(Stock):

  stocks = {'Apple': 'AAPL', 'Airbus': 'AIR.BE', 'AMD': 'AMD', 'Boeing': 'BA', 'BMW': 'BMW.BE', 'Facebook': 'FB', 'Google': 'GOOG', 'IBM': 'IBM', 
      'Intel': 'INTC', 'Jumia': 'JMIA', 'Microsoft': 'MSFT', 'Nvidia': 'NVDA', 'Samsung': '005930.KS', 'Tesla': 'TSLA', 'Twitter': 'TWTR', 'Uber': 'UBER',
      'Volkswagen': 'VOW.DE'}

  for stock, ticker in stocks.items():
        if Stock == stock:
            return ticker

def stock_crypto_markets(Exchange):

    bittrex_markets = ('Bitcoin','Ethereum','Tether','US Dollar')

    binance_markets = ('Binance Coin','Binance USD','Bitcoin','Ethereum','Nigerian Nira','Paxos Standard','Ripple','Russian Ruble','Stable USD',
                    'Tether','Tron','TrueUSD','USD Coin')

    bitfinex_markets = ('Bitcoin','British Pound','Ethereum','Japanese Yen','US Dollar')

    bitfinex_markets_not_working = ('EOS','Euro','Ishares China Index ETF','Stable USD','Stellar','Tether','Ultra Salescloud')

    yahoo_stocks = ('AMD', 'Airbus', 'Apple', 'BMW', 'Boeing', 'Facebook', 'Google', 'IBM', 'Intel', 'Jumia', 'Microsoft', 'Nvidia', 'Samsung', 
                    'Tesla', 'Twitter', 'Uber', 'Volkswagen')

    if Exchange == 'Bittrex':
        market = bittrex_markets
    elif Exchange == 'Binance':
         market = binance_markets
    elif Exchange == 'Bitfinex':
        market = bitfinex_markets
    elif Exchange == 'Yahoo Finance':
        market = yahoo_stocks

    return market

def crypto_markets_to_ticker(Market):

    markets = {'Bitcoin':'BTC','Ethereum':'ETH','Tether':'USDT','Binance Coin':'BNB','Ripple':'XRP','US Dollar':'USD',
            'TrueUSD':'TUSD','Euro':'EUR','British Pound':'GBP','Russian Ruble':'RUB','Nigerian Nira':'NGN','Stellar':'XLM',
            'Japanese Yen':'JPY','Paxos Standard':'PAX','USD Coin':'USDC','Stable USD':'USDS','Binance USD':'BUSD',
            'Tron':'TRX','Ishares China Index ETF':'XCH','Ultra Salescloud':'UST'}

    for market, ticker in markets.items():
        if Market == market:
            return ticker

def bittrex_coins(Market):

    bittrex_btc_options = ('0x','12Ships','Abyss Token','AdEx','Aeon','Akropolis','Ankr','Aragon','Ardor','Ark','Augur','BANKEX','BLOCKv','BORA',
    'BTU Protocol','Bancor','Basic Attention Token','BitShares','BitTorrent','BitTube','Bitcoin Cash','Bitcoin SV',
    'BlackCoin','Blockcloud','Blocknet','BnkToTheFuture','Burst','Bytom','Cardano','Chainlink','Chromia','Cindicator','Civic',
    'Cortex','Cosmo Coin','Cosmos','Cred','Crowd Machine','Crown','Crypto.com Coin','Curecoin','DATA','DECENT','DMarket','Dash',
    'Decentraland','Decred','Dent','DigiByte','DigitalNote','Dogecoin','Dragonchain','Dusk Network','EOS','Edgeless',
    'Einsteinium','Endor Protocol','Enigma','Enjin Coin','Ethereum','Ethereum Classic','ExclusiveCoin','Expanse','FLETA','FLO',
    'FNB Protocol','Factom','Feathercoin','FirstBlood','Flexacoin','Function X','GameCredits','GeoCoin','Gifto','Gnosis',
    'GoChain','Golem','Grin','Groestlcoin','Gulden','Haven Protocol','Hdac','Hedera Hashgraph','HedgeTrade','Horizen',
    'Humaniq','Hxro','Hydro','I/O Coin','IHT Real Estate Protocol','ION','IOST','Ignis','Incent','IoTeX','Jibrel Network',
    'Komodo','LBRY Credits','LUNA','Lambda','Lisk','Litecoin','Loom Network','Loopring','MCO','Maecenas','MaidSafeCoin',
    'Mainframe','Memetic / PepeCoin','Mercury','Metadium','Metal','Metronome','MonaCoin','Monero','MonetaryUnit','More Coin',
    'Morpheus.Network','Multi-collateral DAI','Myriad','NEM','NEO','NKN','NavCoin','Nexus','NoLimitCoin','Numeraire','Nxt',
    'OKCash','OST','Obyte','Ocean Protocol','OmiseGO','Ontology','Ontology Gas','Orbs','OriginTrail','PAL Network','PCHAIN',
    'PIVX','PIXEL','Particl','Patientory','Paxos Standard','Peercoin','Pinkcoin','PlayChip','Pledge Coin','PotCoin','Prometeus',
    'PumaPay','Pundi X','Qtum','Quant','Quantum Resistant Ledger','Radium','Ravencoin','ReddCoin','Refereum',
    'Ripio Credit Network','SIBCoin','SIRIN LABS Token','SIX','SOLVE','STPT','SaluS','Sentinel Protocol','Siacoin',
    'SpaceChain','Spendcoin','Sphere','StableUSD','Status','Stealth','Steem','Steem Dollars','Stellar','Storj','Storm','Stratis',
    'Syscoin','TEMCO','TRON','TTC','TenX','Tezos','TrueUSD',"Tutor's Diary",'Ubiq','Unikoin Gold','Uranus','Utrust','VITE',
    'VeChain','Verge','VeriBlock','VeriCoin','Vertcoin','Viacoin','Viberate','Vodi X','W Green Pay','WAX','Waves','XEL','XRP',
    'Zcash','Zcoin','Zilliqa','adToken','aelf','district0x','iExec RLC')

    bittrex_eth_options = ('0x','AdEx','Aragon','Augur','Basic Attention Token','Bitcoin Cash','Bitcoin SV','Cardano','Civic','Cosmos','DMarket',
    'Dash','Decentraland','DigiByte','EOS','Enigma','Ethereum Classic','Function X','Gnosis','Golem','Hedera Hashgraph',
    'Litecoin','MCO','Monero','Multi-collateral DAI','NEM','NEO','OmiseGO','Pundi X','Qtum','SIRIN LABS Token','SOLVE',
    'Siacoin','Status','Stellar','Storm','Stratis','TRON','TenX','Tezos','TrueUSD','Unikoin Gold','Viberate','Vodi X','WAX',
    'Waves','XRP','Zcash')

    bittrex_usdt_options = ('0x','Basic Attention Token','BitTorrent','Bitcoin','Bitcoin Cash','Bitcoin SV','Cardano','Cosmos','Dash','Decred',
    'DigiByte','Dogecoin','EOS','Enjin Coin','Ethereum','Ethereum Classic','Grin','Hedera Hashgraph','Litecoin','Monero',
    'Multi-collateral DAI','NEO','Ocean Protocol','OmiseGO','Ontology','PumaPay','Pundi X','Ravencoin','Siacoin','Stellar',
    'TRON','Tezos','TrueUSD','VeChain','Verge','Vodi X','XRP','Zcash')

    bittrex_usd_options = ('0x','Basic Attention Token','Bitcoin','Bitcoin Cash','Bitcoin SV','Cardano','Decred','DigiByte','Ethereum',
    'Ethereum Classic','Hedera Hashgraph','Horizen','Komodo','Litecoin','Paxos Standard','Siacoin','TRON','Tether',
    'Tezos','TrueUSD','XRP','Zcash')

    if Market == 'Bitcoin':
        coins = bittrex_btc_options
    elif Market == 'Ethereum':
        coins = bittrex_eth_options
    elif Market == 'Tether':
        coins = bittrex_usdt_options
    elif Market == 'USD':
        coins = bittrex_usd_options

    return coins

def binance_coins(Market):

    binance_btc_options = ('0x','ARPA Chain','Aave','AdEx','Aeron','Aeternity','Agrello','Aion','AirSwap','Algorand','Ambrosus','Ankr','AppCoins',
    'Ardor','Ark','Augur','Bancor','Band Protocol','Basic Attention Token','Beam','Binance Coin','BitShares','Bitcoin Cash',
    'Bitcoin Diamond','Bitcoin Gold','Blockmason Credit Protocol','Blockstack','Blox','Bluzelle','Bread''Cardano',
    'Celer Network','Chainlink','Chiliz','Cindicator','Civic','Cocos-BCX','Contentos','Cortex','Cosmos','CyberMiles','Dash',
    'Decentraland','Decred','DigixDAO','Dock','Dogecoin','Dusk Network','EOS','Eidoo','Elrond','Enigma','Enjin Coin',
    'Ethereum','Ethereum Classic','Etherparty','Everex','FTX Token','Fantom','Fetch.ai','FunFair','GXChain','Gas',
    'Genesis Vision','Gifto','GoChain','Golem','Groestlcoin','Harmony','Hedera Hashgraph','Holo','Horizen','HyperCash',
    'ICON','IOST','IOTA','Insolar','IoTeX','Kava','Komodo','Kyber Network','Lisk','Litecoin','Loom Network','Loopring',
    'Lunyr','MCO','Mainframe','Matic Network','Metal','Mithril','Moeda Loyalty Points','Monero','Monetha','NEM','NEO','NKN',
    'NULS','Nano','NavCoin','Neblio','Nebulas','Nexus','Nucleus Vision','OAX','OST','OmiseGO','Ontology','Ontology Gas','PIVX',
    'POA','Perlin','Po.et','Polymath','Populous','Power Ledger','QLC Chain','Qtum','Quantstamp','QuarkChain',
    'Raiden Network Token','Ravencoin','Red Pulse Phoenix','Ren','Request','Ripio Credit Network','SONM','Selfkey','Siacoin',
    'SingularDTV','SingularityNET','Skycoin','Status','Steem','Stellar','Storj','Storm','Stratis','Streamr DATAcoin','Syscoin',
    'THETA','TRON','TROY','Tael','Tezos','Theta Fuel','Tierion','Time New Bank','TomoChain','VIBE','VITE','VeChain','Verge',
    'Viacoin','Viberate','Voyager Token','Waltonchain','Wanchain''Waves','WePower','XRP','YOYOW','Zcash','Zcoin','Zilliqa',
    'aelf','district0x','iExec RLC')

    binance_eth_options = ('0x','Aave','AdEx','Aeron','Aeternity','Agrello','Aion','AirSwap','Ambrosus','AppCoins','Ardor','Ark','Augur','Bancor',
    'Basic Attention Token','Binance Coin','BitShares','Bitcoin Diamond','Bitcoin Gold','Blockmason Credit Protocol','Blox',
    'Bluzelle','Bread','Cardano','Chainlink','Cindicator','Civic','CyberMiles','Dash','Decentraland','Dent','DigixDAO','Dock',
    'EOS','Eidoo','Enigma','Enjin Coin','Ethereum Classic','Everex','FunFair','GXChain','Genesis Vision','Gifto','Golem',
    'Groestlcoin','Holo','Horizen','HyperCash','ICON','IOST','IOTA','Insolar','IoTeX','Komodo','Kyber Network','Lisk',
    'Litecoin','Loom Network','Loopring','MCO','Mainframe','Metal','Metal','Moeda Loyalty Points','Monero','Monetha','NEM',
    'NEO','NULS','Nano','Neblio','Nebulas','Nexus','Nucleus Vision','OAX','OST','OmiseGO','Ontology','PIVX','POA','Po.et',
    'Populous','Power Ledger','Pundi X','QLC Chain','Qtum','Quantstamp','QuarkChain','Raiden Network Token','Request',
    'Ripio Credit Network','SONM','Selfkey','Siacoin','SingularityNET','Skycoin','Status','Steem','Stellar','Storj','Storm',
    'Stratis','Streamr DATAcoin''Syscoin','THETA','TRON','Tael','Tierion','Time New Bank','VIBE','VeChain','Verge','Viacoin',
    'Viberate','Voyager Token','Waltonchain','Wanchain','Waves','WePower','XRP','YOYOW','Zcash','Zcoin','Zilliqa','aelf',
    'district0x','iExec RLC')

    binance_usdt_options = ('0x','ARPA Chain','Algorand','Ankr','Band Protocol','Basic Attention Token','Beam','Binance Coin','Binance USD',
    'BitTorrent','Bitcoin','Bitcoin Cash','Blockstack','Cardano','Celer Network','Chainlink','Chiliz','Civic','Cocos-BCX',
    'Contentos','Cortex','Cosmos','Dash','Dent','Dock','Dogecoin','Dusk Network','EOS','Elrond','Enjin Coin','Ethereum',
    'Ethereum Classic','FTX Token','Fantom','Fetch.ai','FunFair','Gifto','Harmony','Hedera Hashgraph','Holo','HyperCash',
    'ICON','IOST','IOTA','IoTeX','Kava','Litecoin','MCO','Mainframe','Matic Network','Metal','Mithril','Monero','NEO','NKN',
    'NULS','Nano','OmiseGO','Ontology','Ontology Gas','Paxos Standard','Perlin','Pundi X','Qtum','Ravencoin','Ren','Selfkey',
    'StableUSD','Stellar','Storm','THETA','TRON','TROY','Tezos','Theta Fuel','TomoChain','TrueUSD','USD Coin','VITE','VeChain',
    'WINk','Wanchain','Waves','XRP','Zcash','Zilliqa','iExec RLC')

    binance_bnb_options = ('0x','ARPA Chain','Aeternity','Agrello','Aion','Algorand','Ambrosus','Ankr','AppCoins','Band Protocol',
    'Basic Attention Token','Beam','BitTorrent','Bitcoin Cash','Blockmason Credit Protocol','Blockstack','Bread','Cardano',
    'Celer Network','Chiliz','Cindicator','Cocos-BCX','Contentos','Cortex','Cosmos','CyberMiles','Dash','Decred','Dogecoin',
    'Dusk Network','EOS','Elrond','Enjin Coin','Ethereum Classic','FTX Token','Fantom','Fetch.ai','Gifto','GoChain','Harmony',
    'Hedera Hashgraph','Holo','Horizen','ICON','IOST','IOTA','Kava','Lisk','Litecoin','Loom Network','MCO','Mainframe',
    'Matic Network','Mithril','Monero','NEM','NEO','NKN','NULS','Nano','Neblio','Nebulas','Nexus','OST','OmiseGO','Ontology',
    'Ontology Gas','PIVX','Perlin','Polymath','Power Ledger','QLC Chain','Qtum','Quantstamp','Raiden Network Token',
    'Ravencoin','Red Pulse Phoenix','Ren','Ripio Credit Network','Siacoin','SingularityNET','Skycoin','Steem','Stellar',
    'Storm','Syscoin','THETA','TRON','TROY','Tael','Tezos','Theta Fuel','TomoChain','VITE','VeChain','Viacoin','WINk',
    'Wanchain','Waves','XRP','YOYOW','Zcash','Zcoin','Zilliqa','iExec RLC')

    binance_pax_options = ('Algorand','Basic Attention Token','Binance Coin','BitTorrent','Bitcoin','Bitcoin Cash','Cardano','Chainlink',
    'Dusk Network','EOS','Ethereum','Litecoin','NEO','Ontology','StableUSD','Stellar','TRON','USD Coin','XRP','Zcash')

    binance_tusd_options = ('Algorand','Basic Attention Token','Binance Coin','BitTorrent','Bitcoin','Bitcoin Cash','Cardano','Chainlink','Cosmos',
    'EOS','Ethereum','Ethereum Classic','Litecoin','NEO','Paxos Standard','Red Pulse Phoenix','StableUSD','Stellar','TRON',
    'USD Coin','Waves','XRP','Zcash')

    binance_usdc_options = ('Algorand','Basic Attention Token','Binance Coin','Binance GBP Stable Coin','BitTorrent','Bitcoin','Bitcoin Cash',
    'Cardano','Chainlink','Cosmos','Dusk Network','EOS','Ethereum','Fantom','Harmony','Litecoin','NEO','Ontology','StableUSD',
    'Stellar','TRON','TomoChain','WINk','Waves','XRP','Zcash')

    binance_usds_options = ('Binance Coin', 'Bitcoin')

    binance_ngn_options = ('Binance Coin', 'Binance USD', 'Bitcoin')

    binance_busd_options = ('Binance Coin','Bitcoin','Bitcoin Cash','Cardano','Chainlink','EOS','Ethereum','Ethereum Classic',
                            'Litecoin','Qtum','Stellar','TRON','VeChain','XRP')

    binance_rub_options = ('Binance Coin', 'Binance USD', 'Bitcoin', 'Ethereum', 'XRP')

    binance_trx_options = ('BitTorrent', 'WINk')

    binance_xrp_options = ('TRON', 'Zcoin')

    if Market == 'Bitcoin':
        coins = binance_btc_options
    elif Market == 'Ethereum':
        coins = binance_eth_options
    elif Market == 'Tether':
        coins = binance_usdt_options
    elif Market == 'Binance Coin':
        coins = binance_bnb_options
    elif Market == 'Paxos Standard':
        coins = binance_pax_options
    elif Market == 'TrueUSD':
        coins = binance_tusd_options
    elif Market == 'USD Coin':
        coins = binance_usdc_options
    elif Market == 'StableUSD':
        coins = binance_usds_options
    elif Market == 'Nigerian Nira':
        coins = binance_ngn_options
    elif Market == 'Binance USD':
        coins = binance_busd_options
    elif Market == 'Russian Ruble':
        coins = binance_rub_options
    elif Market == 'Tron':
        coins = binance_trx_options
    elif Market == 'Ripple':
        coins = binance_xrp_options

    return coins

def bitfinex_coins(Market):

    bitfinex_btc_options = ('0Chain','0x','AidCoin','Aion','Algorand','Ampleforth','Aragon','Auctus','Augur','Aventus','BLOCKv','Bancor',
    'Basic Attention Token','BitTorrent','Bitcoin Cash','Bitcoin Gold','Bitcoin Interest','Bitcoin SV','BnkToTheFuture',
    'Callisto Network','Cindicator','CommerceBlock','Cortex','Cosmos','DATA','Dash','Decentraland','Dether','DigiByte',
    'Dusk Network','EOS','Edge','Eidoo','Essentia','Ethereum','Ethereum Classic','Everipedia','FunFair','Fusion','Golem',
    'Hydro Protocol','IOST','IOTA','Kyber Network','Litecoin','Loopring','Lympo','Maker','Medicalchain','Metaverse ETP',
    'Mithril','Monero','Multi-collateral DAI','NEO','Nectar','Nucleus Vision','ODEM','OKB','ORS Group','OmiseGO','Omni','POA',
    'Polymath','Project Pai','QASH','Qtum','RIF Token','RSK Smart Bitcoin','Raiden Network Token','Request',
    'Ripio Credit Network','SEER','Santiment Network Token','SingularDTV','SingularityNET','SpankChain','Status','Stellar',
    'Storj','Streamr DATAcoin','TRON','Tezos','Time New Bank','UNUS SED LEO','USDK','Ultra','Utrust','V Systems','VeChain',
    'Verge','WAX','WePower','XRP','YOYOW','Zcash','Zilliqa','aelf','iExec RLC')

    bitfinex_eth_options = ('0Chain','0x','Abyss Token','AidCoin','Aion','AirSwap','Aragon','Auctus','Augur','Autonio','Aventus','BLOCKv','Bancor',
    'Banyan Network','Basic Attention Token','Blockpass','BnkToTheFuture','Cindicator','CommerceBlock',
    'Content Neutrality Network','ContentBox','Cortex','Cosmos','Credits','CryptoFranc','DAOstack','DATA','Decentraland',
    'Dether','Digix Gold Token','Dragonchain','EOS','Edge','Eidoo','Enjin Coin','Essentia','Ether Kingdoms Token','FOAM',
    'FunFair','Fusion','Gnosis','Golem','Hydro Protocol','INT Chain','IOST','IOTA','Kleros','Kyber Network','Loom Network',
    'Loopring','Lympo''Maker','Matrix AI Network','Medicalchain','Melon','Metaverse ETP','Mithril','MobileGo','Monolith',
    'Multi-collateral DAI','NEO','Nectar','Nucleus Vision','ODEM','OKB','ORS Group','OmiseGO','On.Live','POA','ParkinGo',
    'Polymath','QASH','Qtum','Raiden Network Token','Rate3','Request','Ripio Credit Network','SEER','STASIS EURO',
    'Santiment Network Token','SingularDTV','SingularityNET','SpankChain','Status','Stellar','Storj','Streamr DATAcoin',
    'Swarm','TRON','Time New Bank','Tripio','UNUS SED LEO','USDK','Universa','Upfiring','Utrust','VeChain','Verge','Vetri',
    'WAX','Waltonchain','WePower','Wrapped Bitcoin','Xriba','YGGDRASH','YOYOW','Zilliqa','aelf''iExec RLC')

    bitfinex_usdt_options = ('Algorand','Ampleforth','BitKan','Bitcoin','Bitcoin Cash','Dragon Token','EOS','Ethereum',
                            'FTX Token','Litecoin','OKB','UNUS SED LEO','USDK')

    bitfinex_usd_options = ('0Chain','0x','Abyss Token','AidCoin','Aion','AirSwap','Algorand','Ampleforth','Aragon','Atonomi','Auctus','Augur',
    'Autonio','Aventus','BLOCKv','Bancor','Banyan Network','Basic Attention Token','BitKan','BitTorrent','Bitcoin',
    'Bitcoin Cash','Bitcoin Gold','Bitcoin Interest','Bitcoin SV','Blockpass','BnkToTheFuture','Callisto Network','Cindicator',
    'CommerceBlock','Content Neutrality Network','ContentBox','Cortex','Cosmos','Credits','CryptoFranc','DAOstack','DATA','Dash',
    'Decentraland','Dether','DigiByte','Digix Gold Token','Dragon Token','Dragonchain','Dusk Network','EOS','Edge','Eidoo',
    'Enjin Coin','Essentia','Ether Kingdoms Token','Ethereum','Ethereum Classic','Everipedia','FOAM','FTX Token','FunFair',
    'Fusion','Gemini Dollar','Gnosis','Golem','Hydro Protocol','INT Chain','IOST','IOTA','Kleros','Kyber Network','Litecoin',
    'Loom Network','Loopring','Lympo','Maker','Matrix AI Network','Medicalchain','Melon','Metaverse ETP','Mithril','MobileGo',
    'Monero','Monolith','Multi-collateral DAI','NEO','Nectar','Nucleus Vision','ODEM','OKB','ORS Group','OmiseGO','Omni',
    'On.Live','POA','ParkinGo','Paxos Standard','Polymath','Project Pai','QASH','Qtum','RIF Token','RSK Smart Bitcoin',
    'Raiden Network Token','Rate3','Request','Ripio Credit Network','SEER','STASIS EURO','Santiment Network Token',
    'SingularDTV','SingularityNET','SpankChain','Status','Stellar','Storj','Streamr DATAcoin','Swarm','TRON','Tether','Tezos',
    'Time New Bank','Tripio','TrueUSD','UNUS SED LEO','USD Coin','USDK','Ultra','Universa','Upfiring','Utrust','V Systems',
    'VeChain','Verge','Vetri','WAX','WOLLO','Waltonchain','WePower','Wrapped Bitcoin','XRP','Xriba','YGGDRASH','YOYOW',
    'ZB Token','Zcash','Zilliqa','aelf','iExec RLC')

    bitfinex_xch_options = ('Bitcoin')

    bitfinex_eur_options = ('Bitcoin','EOS','Ethereum','IOTA','NEO','ParkinGo','Stellar','TRON','Verge')

    bitfinex_jpy_options = ('Bitcoin', 'EOS', 'Ethereum', 'IOTA', 'NEO', 'Stellar', 'TRON', 'Verge')

    bitfinex_gbp_options = ('Bitcoin', 'EOS', 'Ethereum', 'IOTA', 'NEO', 'Stellar', 'TRON', 'Verge')

    bitfinex_eos_options = ('Everipedia', 'UNUS SED LEO', 'USDK')

    bitfinex_xlm_options = ('WOLLO')

    bitfinex_ust_options = ('ZB Token')

    if Market == 'Bitcoin':
        coins = bitfinex_btc_options
    elif Market == 'Ethereum':
        coins = bitfinex_eth_options
    elif Market == 'Tether':
        coins = bitfinex_usdt_options
    elif Market == 'US Dollar':
        coins = bitfinex_usd_options
    elif Market == 'Ishares China Index ETF':
        coins = bitfinex_xch_options
    elif Market == 'Japanese Yen':
        coins = bitfinex_jpy_options
    elif Market == 'British Pound':
        coins = bitfinex_gbp_options
    elif Market == 'EOS':
        coins = bitfinex_eos_options
    elif Market == 'Stellar':
        coins = bitfinex_xlm_options
    elif Market == 'Ultra Salescloud':
        coins = bitfinex_ust_options

    return coins

def exchange_to_coins_loading (Exchange, Market):

    if Exchange == 'Bittrex':
        coins = bittrex_coins(Market)
    elif Exchange == 'Binance':
         coins = binance_coins(Market)
    elif Exchange == 'Bitfinex':
        coins = bitfinex_coins(Market)

    return coins

def yahoo_interval(Interval):

    if Interval == '1 Minute':
        period = '7d'
    elif Interval == '5 Minute' or Interval == '15 Minute' or Interval == '30 Minute':
        period = '1mo'
    elif Interval == '1 Hour':
        period = '2y'
    else:
        period = 'max'

    intervals = {'1 Minute':'1m', '5 Minute':'5m', '15 Minute':'15m', '30 Minute':'30m', 
                '1 Hour':'60m', '1 Day':'1d', '1 Week':'1wk', '1 Month':'1mo'}

    for interval, inter in intervals.items():
        if Interval == interval:
            stock_interval = inter

    return period, stock_interval

def crypto_interval(Exchange, Interval):

    intervals = {'1 Minute':'1m', '5 Minute':'5m', '15 Minute':'15m', '30 Minute':'30m', 
    '1 Hour':'1h', '1 Day':'1d', '1 Week':'1w', '1 Month':'1M'}

    bittrex_intervals = {'1 Minute':'oneMin', '5 Minute':'fiveMin', '30 Minute':'thirtyMin', 
    '1 Hour':'hour', '1 Day':'day'}

    if Exchange == 'Bittrex':
        for bitt_interval, bitt_inter in bittrex_intervals.items():
            if Interval == bitt_interval:
                bittrex_interval = bitt_inter
        
            return  bittrex_interval
        
    else:
        for interval, inter in intervals.items():
            if Interval == interval:
                crypto_interval = inter
            return crypto_interval
