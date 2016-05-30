# PNAX Network Analyzer

reference the programming manual here: http://na.support.keysight.com/pna/help/index.html?id=1000001808-1:epsg:man
and specifically here: New Programming Commands:
http://na.support.keysight.com/pna/help/latest/help.htm


## Example Usage

The driver is optimized to make the least amount of queries to the PNA-X 
while taking data. For this reason, the way you take single shot data is 
a bit different from taking data in a for loop.

### Single Shot Example
```python
__author__ = 'Ge Yang'

from Instruments import N5242A
from time import sleep
import matplotlib.pyplot as plt

nwa = N5242A(address="192.168.14.249")
print nwa.get_id()

nwa.set_query_timeout(10000)
nwa.set_sweep_points(2000)

# this is always going to give an error message regardless
nwa.clear_traces()
nwa.setup_measurement("S21")

plt.figure()
data = nwa.take_one_in_mag_phase()
plt.plot(data[1])
plt.show()
```

### Taking Data in a For-loop

```python
#  this one sets the averaging
nwa.set_averages_and_group_count(50)    
nwa.setup_take()
for i in range(1000):
    # giving the take command a `sweep_points` parameter speeds up the 
    # data taking, because it doesn't need to query the PNA-X to figure 
    # it out
    sweep_points = 1000
    data = nwa.take(sweep_points)
    # do whatever you want with the data.
```


## Important Notes