# pyfcomb: Easy frequency combinations

Frequency combinations made easy! pyfcomb allows you to compute possible combinations of 
frequencies from a given list of frequencies. 

## Installation
Call
```
pip install pyfcomb
```
to install pyfcomb.

## Usage
Use 
```python
pyfcomb.get_combinations(f_ids,frequencies,amplitudes)
```
 to compute the combinations. You need to provide a list of frequency ids, frequencies and
 amplitudes all of the same length to compute combinations. You can also use the ```combo_depth```
 parameter to change the maximum amount of combinations as well as the ```accuracy``` parameter
 to change the minimum precision of combinations.
 
 The function then returns a ```pandas.DataFrame``` consisting of all frequencies and their 
 possible combinations. The best combination (in this case the one with highest precision and least
 complexity) is also used to calculate the residual from the actual frequency to the combination. Lastly,
 this DataFrame also contains a list of all other possible combinations.
 
 ### Example
 ```python
from pyfcomb import get_combinations
from pandas import read_csv

file = read_csv("pyfcomb/tests/testfiles/freq_data.txt",delimiter="\t",header=None,names=['f_num','f','amp','snr'])
f_num = [int(i.replace("F","")) for i in file.f_num]
combinations = get_combinations(f_num,file.f,file.amp)
```