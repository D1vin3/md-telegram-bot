import emoji


# Main Buttons when bot /start/
main_buttons = [
    '{} Купить'.format(emoji.emojize(':shopping_cart:')),
    '{} Продать'.format(emoji.emojize(':money_bag:', use_aliases=True)),
    '{} Мои_объявления'.format(emoji.emojize(':package:', use_aliases=True))
]

main_buttons_without_img = [
    '/Купить',
    '/Продать',
    '/Мои_объявления'
]

crypto_sell_buttons = [
    '1. Bitcoin (BTC)',
    '2. Ethereum (ETH)',
    '3. Bitcoin Cash (BCH)',
    '4. Ripple (XRP)',
    '5. Litecoin (LTC)',
    '6. Cardano (ADA)',
    '7. IOTA (MIOTA)',
    '8. Dash (DASH)',
    '9. NEM (XEM)',
    '10. Monero (XMR)',
    '11. Bitcoin Gold (BTG)',
    '12. EOS (EOS)',
    '13. Stellar (XLM)',
    '14. Neo (NEO)',
    '15. Qtum (QTUM)',
    '16. Ethereum Classic (ETC)',
    '17. Verge (XVG)',
    '18. TRON (TRX)',
    '19. Lisk (LSK)',
    '20. Nxt (NXT)',
    '21. Zcash (ZEC)',
    '22. BitConnect (BCC)',
    '23. OmiseGO (OMG)',
    '24. Waves (WAVES)',
    '25. Populous (PPT)',
    '26. Другой (свой вариант)',
]

currency_site_buttons = [
    '1. blockchain.info',
    '2. bittrex.com',
    '3. bitfinex.com',
    '4. poloniex.com',
    '5. exmo.com',
    '6. cex.io',
    '7. yobit.net',
    '8. Другой',
]

currency_site_buttons_html = [
    '<a>blockchain.info</a>',
    # '<a href="http://bittrex.com">bittrex.com</a>',
    # '<a href="http://bitfinex.com">bitfinex.com</a>'
    # '<a href="http://blockchain.info">blockchain.info</a>',
    # '<a href="http://blockchain.info">blockchain.info</a>',
    # '<a href="http://blockchain.info">blockchain.info</a>',
    # '<a href="http://blockchain.info">blockchain.info</a>',
    # '<a href="http://blockchain.info">blockchain.info</a>',
]

marginality_amount_buttons = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'более 10']
