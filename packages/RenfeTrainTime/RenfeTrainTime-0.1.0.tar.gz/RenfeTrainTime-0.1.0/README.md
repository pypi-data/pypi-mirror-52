# Renfe Train Time
renfe-time scrapes and parses train schedules for RENFE trains in Spain. At the moment, only Asturias is supported

### Usage
```python
from RenfeTrainTime import RenfeTime as rt
from datetime import datetime
import pprint

table = rt.getTimeTable(
    rt.getStationCode( "Gijón" ),
    rt.getStationCode( "Oviedo" ),
    datetime.now(), "00", "26", False
)

pprint.pprint( table, indent = 4 )
```
