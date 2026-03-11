
# Algo Trading Proyect

This project its mean to be a really simple starting on Algo Trading.
Will run on an infinite loop and will be testing/using strategies.


## Platform
It will use the platform Trading212 new api

## Improvements

Create strategies by json format:
```
{
  "name": "Strategia prueba",
  "ticker_api": "AAPL_US_EQ",
  "ticker_data": "AAPL",
  "indicators": { "EMA": [10, 25] },
  "interval": "1m",
  "period": "1D",
  "entry_rule": { "type": "ema_cross_above", "fast": 10, "slow": 25 },
  "exit_rule": { "type": "ema_cross_above", "fast": 10, "slow": 25 }
}
```
There are also AND and OR functions possible to use:
```
"entry_rule": {
        "type": "AND",
        "signals": [
            {
                "type": "EMACross",
                "fast": 10,
                "slow": 25
            },
            {
                "type": "RSI",
                "period": 14,
                "threshold": 30
            }
        ]
    },
```

## Working code

Arquitecture: 
```
TradingEngine            # Controls the API and total money    
    └── StrategyManager  # Controls One single strategy
        └── DataManager  # Each strategy uses its own data manager
```
## Trading_API

Improve documentation of each function for the arguments

```
trading_api/                # Tu paquete personalizado
    ├── __init__.py         # Hace que la carpeta sea un paquete
    ├── base.py             # Manejo de headers y peticiones base
    ├── accounts.py         # Funciones de cuenta y balance
    ├── instruments.py      # Metadata, tickers y horarios
    ├── historical_events.py 
    ├── positions.py       
    └── orders.py           # Compra, venta y cancelaciones
```


Collection of all possible calls to the Trading212 API

