base = 'BTC'
    
os.system('curl -H "X-CMC_PRO_API_KEY: '+cmckey+'"  -H "Connection: keep-alive" -H "Accept: application/json" -d "start=1&limit=100&convert='+base+'" -G https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest > '+file)  
df =  json.load(open(file))
ret = []
for coin in df['data']:
    new = {}
    for key in coin:
        if key not in('quote', 'tags', 'platform'): 
            new[key] = coin[key]
    if len(coin['quote']) > 0:
        for k in coin['quote'][base]:
            new[k] = coin[key][base][k]
    ret.append(new)
pd.DataFrame(ret)

df = df[((df['percent_change_24h'] < game['24floor']) & (df['cmc_rank'] < 100))]
df['vol'] = df['volume_24h'] / df['market_cap']
df = df[df['vol']>0.1]
df = df.to_dict(orient='records')
prices = getBinacePrices()
for row in df:
    if row['symbol'] in prices:
        cmd = '''curl --location --request POST 'https://3commas.io/trade_signal/trading_view' --header 'Content-Type: text/plain' --data-raw \'{"message_type": "bot","bot_id": '''+str(game['BOT'])+''',"email_token": "'''+str(game['token'])+'''","delay_seconds": 0,"pair": "'''+base+'_'+row['symbol']+'''"}\' '''
        os.system(cmd)
