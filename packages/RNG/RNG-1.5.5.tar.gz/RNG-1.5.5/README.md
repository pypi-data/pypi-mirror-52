# Random Number Generator Engine for Python3
- Compiled Python3 API for the C++ Random Library
- Designed for python developers familiar with C++ Random.h
- Warning: RNG is not suitable for cryptography or secure hashing

### Sister Projects:
- Fortuna: Collection of tools to make custom random value generators. https://pypi.org/project/Fortuna/
- Pyewacket: Drop-in replacement for the Python3 random module. https://pypi.org/project/Pyewacket/
- MonkeyScope: Framework for testing non-deterministic value generators. https://pypi.org/project/MonkeyScope/

Support these and other random projects: https://www.patreon.com/brokencode

### Quick Install
``` 
$ pip install RNG
$ python3
>>> import RNG ...
```

### Installation may require the following:
- Python 3.7 or later with dev tools (setuptools, pip, etc.)
- Cython: `pip install Cython`
- Modern C++17 compiler and standard library for your platform.


---

## RNG Specifications

#### Random Boolean
- `RNG.bernoulli_variate(ratio_of_truth: float) -> bool`
    - Produces a Bernoulli distribution of boolean values.
    - @param ratio_of_truth :: the probability of True. Expected input range: `[0.0, 1.0]`, clamped.
    - @return :: True or False


#### Random Integer
- `RNG.uniform_int_variate(left_limit: int, right_limit: int) -> int`
    - Flat uniform distribution.
    - 20x faster than random.randint()
    - @param left_limit :: input A.
    - @param right_limit :: input B. 
    - @return :: random integer in the inclusive range `[A, B]` or `[B, A]` if B < A
- `RNG.binomial_variate(number_of_trials: int, probability: float) -> int`
    - Based on the idea of flipping a coin and counting how many heads come up after some number of flips.
    - @param number_of_trials :: how many times to flip a coin.
    - @param probability :: how likely heads will be flipped. 0.5 is a fair coin. 1.0 is a double headed coin.
    - @return :: count of how many heads came up.
- `RNG.negative_binomial_variate(trial_successes: int, probability: float) -> int`
    - Based on the idea of flipping a coin as long as it takes to succeed.
    - @param trial_successes :: the required number of heads flipped to succeed.
    - @param probability :: how likely heads will be flipped. 0.50 is a fair coin.
    - @return :: the count of how many tails came up before the required number of heads.
- `RNG.geometric_variate(probability: float) -> int`
    - Same as random_negative_binomial(1, probability). 
- `RNG.poisson_variate(mean: float) -> int`
    - @param mean :: sets the average output of the function.
    - @return :: random integer, poisson distribution centered on the mean.


#### Random Floating Point
- `RNG.generate_canonical() -> float`
    - Evenly distributes floats of maximum precision.
    - @return :: random float in range (0.0, 1.0)
- `RNG.uniform_real_variate(left_limit: float, right_limit: float) -> float`
    - Flat uniform distribution of floats.
    - @return :: random Float between left_limit and right_limit.
- `RNG.normal_variate(mean: float, std_dev: float) -> float`
    - @param mean :: sets the average output of the function.
    - @param std_dev :: standard deviation. Specifies spread of data from the mean.
- `RNG.lognormal_variate(log_mean: float, log_deviation: float) -> float`
    - @param log_mean :: sets the log of the mean of the function.
    - @param log_deviation :: log of the standard deviation. Specifies spread of data from the mean.
- `RNG.exponential_variate(lambda_rate: float) -> float`
    - Produces random non-negative floating-point values, distributed according to probability density function.
    - @param lambda_rate :: λ constant rate of a random event per unit of time/distance.
    - @return :: The time/distance until the next random event. For example, this distribution describes the time between the clicks of a Geiger counter or the distance between point mutations in a DNA strand.
- `RNG.gamma_variate(shape: float, scale: float) -> float`
    - Generalization of the exponential distribution.
    - Produces random positive floating-point values, distributed according to probability density function.    
    - @param shape :: α the number of independent exponentially distributed random variables.
    - @param scale :: β the scale factor or the mean of each of the distributed random variables.
    - @return :: the sum of α independent exponentially distributed random variables, each of which has a mean of β.
- `RNG.weibull_variate(shape: float, scale: float) -> float`
    - Generalization of the exponential distribution.
    - Similar to the gamma distribution but uses a closed form distribution function.
    - Popular in reliability and survival analysis.
- `RNG.extreme_value_variate(location: float, scale: float) -> float`
    - Based on Extreme Value Theory. 
    - Used for statistical models of the magnitude of earthquakes and volcanoes.
- `RNG.chi_squared_variate(degrees_of_freedom: float) -> float`
    - Used with the Chi Squared Test and Null Hypotheses to test if sample data fits an expected distribution.
- `RNG.cauchy_variate(location: float, scale: float) -> float`
    - @param location :: It specifies the location of the peak. The default value is 0.0.
    - @param scale :: It represents the half-width at half-maximum. The default value is 1.0.
    - @return :: Continuous Distribution.
- `RNG.fisher_f_variate(degrees_of_freedom_1: float, degrees_of_freedom_2: float) -> float`
    - F distributions often arise when comparing ratios of variances.
- `RNG.student_t_variate(degrees_of_freedom: float) -> float`
    - T distribution. Same as a normal distribution except it uses the sample standard deviation rather than the population standard deviation.
    - As degrees_of_freedom goes to infinity it converges with the normal distribution.


## Development Log
##### RNG 1.5.5
- Storm Update

##### RNG 1.5.4
- Storm 3.2 Update

##### RNG 1.5.3
- Fixed Typos

##### RNG 1.5.2
- Compiler Config Update

##### RNG 1.5.1
- A number of testing routines have been extracted into a new module: MonkeyScope.
    - distribution
    - timer
    - distribution_timer

##### RNG 1.5.0, internal
- Further API Refinements, new naming convention for variate generators: `<algorithm name>_variate`

##### RNG 1.4.2
- Install script update
- Test tweaks for noise reduction in timing tests.

##### RNG 1.4.1
- Test Patch for new API
- Documentation Updates

##### RNG 1.4.0
- API Refactoring

##### RNG 1.3.4
- Storm Update 3.1.1

##### RNG 1.3.3
- Installer script update

##### RNG 1.3.2
- Minor Bug Fix

##### RNG 1.3.1
- Test Update

##### RNG 1.3.1
- Fixed Typos

##### RNG 1.3.0
- Storm Update

##### RNG 1.2.5
- Low level clean up

##### RNG 1.2.4
- Minor Typos Fixed

##### RNG 1.2.3
- Documentation Update
- Test Update
- Bug Fixes

##### RNG 1.0.0 - 1.2.2, internal
- API Changes:
    - randint changed to random_int
    - randbelow changed to random_below
    - random changed to generate_canonical
    - uniform changed to random_float

##### RNG 0.2.3
- Bug Fixes

##### RNG 0.2.2
- discrete() removed.

##### RNG 0.2.1
- minor typos
- discrete() depreciated.

##### RNG 0.2.0
- Major Rebuild.

##### RNG 0.1.22
- The RNG Storm Engine is now the default standard.
- Experimental Vortex Engine added for testing.

##### RNG 0.1.21 beta
- Small update to the testing suite.

##### RNG 0.1.20 beta
- Changed default inputs for random_int and random_below to sane values.
    - random_int(left_limit=1, right_limit=20) down from `-2**63, 2**63 - 1`
    - random_below(upper_bound=10) down from `2**63 - 1`

##### RNG 0.1.19 beta
- Broke some fixed typos, for a change of pace.

##### RNG 0.1.18 beta
- Fixed some typos.

##### RNG 0.1.17 beta
- Major Refactoring.
- New primary engine: Hurricane.
- Experimental engine Typhoon added: random_below() only.

##### RNG 0.1.16 beta
- Internal Engine Performance Tuning. 

##### RNG 0.1.15 beta
- Engine Testing.

##### RNG 0.1.14 beta
- Fixed a few typos.

##### RNG 0.1.13 beta
- Fixed a few typos.

##### RNG 0.1.12 beta
- Major Test Suite Upgrade.
- Major Bug Fixes.
    - Removed several 'foot-guns' in prep for fuzz testing in future releases.

##### RNG 0.1.11 beta
- Fixed small bug in the install script.

##### RNG 0.1.10 beta
- Fixed some typos.

##### RNG 0.1.9 beta
- Fixed some typos.

##### RNG 0.1.8 beta
- Fixed some typos.
- More documentation added.

##### RNG 0.1.7 beta
- The `random_floating_point` function renamed to `random_float`.
- The function `c_rand()` has been removed as well as all the cruft it required.
- Major Documentation Upgrade.
- Fixed an issue where keyword arguments would fail to propagate. Both, positional args and kwargs now work as intended.
- Added this Dev Log.

##### RNG 0.0.6 alpha
- Minor ABI changes.

##### RNG 0.0.5 alpha
- Tests redesigned slightly for Float functions.

##### RNG 0.0.4 alpha
- Random Float Functions Implemented.

##### RNG 0.0.3 alpha
- Random Integer Functions Implemented.

##### RNG 0.0.2 alpha
- Random Bool Function Implemented.

##### RNG 0.0.1 pre-alpha
- Planning & Design.


## MonkeyScope: Distribution and Performance Test Suite
```
MonkeyScope: RNG Storm Engine
=========================================================================

Boolean Variate Distributions

Output Analysis: bernoulli_variate(0.0)
Typical Timing: 32 ± 12 ns
Statistics of 1024 samples:
 Minimum: False
 Median: False
 Maximum: False
 Mean: 0
 Std Deviation: 0.0
Distribution of 10240 samples:
 False: 100.0%

Output Analysis: bernoulli_variate(0.3333333333333333)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.341796875
 Std Deviation: 0.47454365973544776
Distribution of 10240 samples:
 False: 67.12890625%
 True: 32.87109375%

Output Analysis: bernoulli_variate(0.5)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: False
 Median: False
 Maximum: True
 Mean: 0.486328125
 Std Deviation: 0.5000572731127524
Distribution of 10240 samples:
 False: 50.0390625%
 True: 49.9609375%

Output Analysis: bernoulli_variate(0.6666666666666666)
Typical Timing: 32 ± 14 ns
Statistics of 1024 samples:
 Minimum: False
 Median: True
 Maximum: True
 Mean: 0.6767578125
 Std Deviation: 0.46794285346920644
Distribution of 10240 samples:
 False: 33.134765625%
 True: 66.865234375%

Output Analysis: bernoulli_variate(1.0)
Typical Timing: 32 ± 16 ns
Statistics of 1024 samples:
 Minimum: True
 Median: True
 Maximum: True
 Mean: 1
 Std Deviation: 0.0
Distribution of 10240 samples:
 True: 100.0%


Integer Variate Distributions

Base Case
Output Analysis: Random.randint(1, 6)
Typical Timing: 1157 ± 19 ns
Statistics of 1024 samples:
 Minimum: 1
 Median: 4
 Maximum: 6
 Mean: 3.4658203125
 Std Deviation: 1.6833390080343844
Distribution of 10240 samples:
 1: 16.19140625%
 2: 17.119140625%
 3: 16.38671875%
 4: 16.943359375%
 5: 16.66015625%
 6: 16.69921875%

Output Analysis: uniform_int_variate(1, 6)
Typical Timing: 63 ± 11 ns
Statistics of 1024 samples:
 Minimum: 1
 Median: 3
 Maximum: 6
 Mean: 3.5126953125
 Std Deviation: 1.7192586779476893
Distribution of 10240 samples:
 1: 16.337890625%
 2: 16.5625%
 3: 16.669921875%
 4: 16.748046875%
 5: 16.728515625%
 6: 16.953125%

Output Analysis: binomial_variate(4, 0.5)
Typical Timing: 157 ± 6 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 2
 Maximum: 4
 Mean: 1.9404296875
 Std Deviation: 0.9972426358799124
Distribution of 10240 samples:
 0: 6.15234375%
 1: 24.98046875%
 2: 37.353515625%
 3: 25.0%
 4: 6.513671875%

Output Analysis: negative_binomial_variate(5, 0.75)
Typical Timing: 125 ± 6 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 1
 Maximum: 9
 Mean: 1.6728515625
 Std Deviation: 1.4555671511855643
Distribution of 10240 samples:
 0: 22.96875%
 1: 30.5078125%
 2: 22.978515625%
 3: 12.763671875%
 4: 6.26953125%
 5: 2.666015625%
 6: 1.23046875%
 7: 0.3515625%
 8: 0.13671875%
 9: 0.078125%
 10: 0.029296875%
 11: 0.01953125%

Output Analysis: geometric_variate(0.75)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 0
 Maximum: 6
 Mean: 0.322265625
 Std Deviation: 0.7343361647662979
Distribution of 10240 samples:
 0: 75.078125%
 1: 18.603515625%
 2: 4.609375%
 3: 1.259765625%
 4: 0.33203125%
 5: 0.05859375%
 6: 0.029296875%
 7: 0.01953125%
 8: 0.009765625%

Output Analysis: poisson_variate(4.5)
Typical Timing: 94 ± 13 ns
Statistics of 1024 samples:
 Minimum: 0
 Median: 4
 Maximum: 13
 Mean: 4.4033203125
 Std Deviation: 2.077301032730708
Distribution of 10240 samples:
 0: 1.259765625%
 1: 5.205078125%
 2: 11.025390625%
 3: 16.455078125%
 4: 19.453125%
 5: 17.3046875%
 6: 13.06640625%
 7: 7.490234375%
 8: 4.55078125%
 9: 2.55859375%
 10: 1.03515625%
 11: 0.419921875%
 12: 0.107421875%
 13: 0.0390625%
 14: 0.009765625%
 15: 0.01953125%


Floating Point Variate Distributions

Base Case
Output Analysis: Random.random()
Typical Timing: 32 ± 15 ns
Statistics of 1024 samples:
 Minimum: 0.002212343585933141
 Median: (0.5091348643817574, 0.5098482291995062)
 Maximum: 0.9997233342332014
 Mean: 0.5153782708640672
 Std Deviation: 0.28375024345961336
Post-processor distribution of 10240 samples using round method:
 0: 49.736328125%
 1: 50.263671875%

Output Analysis: generate_canonical()
Typical Timing: 32 ± 16 ns
Statistics of 1024 samples:
 Minimum: 0.00034250343403455485
 Median: (0.49379360389842375, 0.4941647007273199)
 Maximum: 0.9989750152773843
 Mean: 0.49112430693624254
 Std Deviation: 0.28490111696764114
Post-processor distribution of 10240 samples using round method:
 0: 50.439453125%
 1: 49.560546875%

Base Case
Output Analysis: Random.uniform(0.0, 10.0)
Typical Timing: 219 ± 6 ns
Statistics of 1024 samples:
 Minimum: 0.00803046137939023
 Median: (5.097309531471494, 5.103667202591966)
 Maximum: 9.993790772652122
 Mean: 5.105622386544169
 Std Deviation: 2.8609126274855012
Post-processor distribution of 10240 samples using floor method:
 0: 9.94140625%
 1: 9.6484375%
 2: 10.13671875%
 3: 9.62890625%
 4: 9.677734375%
 5: 10.244140625%
 6: 10.107421875%
 7: 10.48828125%
 8: 10.185546875%
 9: 9.94140625%

Output Analysis: uniform_real_variate(0.0, 10.0)
Typical Timing: 32 ± 15 ns
Statistics of 1024 samples:
 Minimum: 0.0036670746870834385
 Median: (5.021081813949522, 5.028910704861424)
 Maximum: 9.999528222086418
 Mean: 5.082930195101253
 Std Deviation: 2.889513696652281
Post-processor distribution of 10240 samples using floor method:
 0: 9.892578125%
 1: 10.25390625%
 2: 9.990234375%
 3: 10.078125%
 4: 9.86328125%
 5: 9.9609375%
 6: 10.361328125%
 7: 10.15625%
 8: 9.853515625%
 9: 9.58984375%

Base Case
Output Analysis: Random.expovariate(1.0)
Typical Timing: 313 ± 16 ns
Statistics of 1024 samples:
 Minimum: 9.062088315521154e-05
 Median: (0.671756407460858, 0.6733751262629283)
 Maximum: 6.269007293381083
 Mean: 0.993478189904074
 Std Deviation: 0.9661183096695404
Post-processor distribution of 10240 samples using floor method:
 0: 62.216796875%
 1: 23.75%
 2: 8.61328125%
 3: 3.466796875%
 4: 1.162109375%
 5: 0.419921875%
 6: 0.234375%
 7: 0.107421875%
 8: 0.029296875%

Output Analysis: exponential_variate(1.0)
Typical Timing: 63 ± 1 ns
Statistics of 1024 samples:
 Minimum: 0.0020525965986051137
 Median: (0.675581567712985, 0.678525371652736)
 Maximum: 6.516268493108022
 Mean: 0.9926867210848236
 Std Deviation: 0.9898570464369526
Post-processor distribution of 10240 samples using floor method:
 0: 63.4765625%
 1: 22.431640625%
 2: 9.0234375%
 3: 3.28125%
 4: 1.064453125%
 5: 0.458984375%
 6: 0.17578125%
 7: 0.05859375%
 8: 0.01953125%
 11: 0.009765625%

Base Case
Output Analysis: Random.gammavariate(1.0, 1.0)
Typical Timing: 469 ± 10 ns
Statistics of 1024 samples:
 Minimum: 0.0009544892911359472
 Median: (0.7209401347760952, 0.7229027330855663)
 Maximum: 13.077468392116579
 Mean: 1.036964163279837
 Std Deviation: 1.089141285068225
Post-processor distribution of 10240 samples using floor method:
 0: 62.71484375%
 1: 23.65234375%
 2: 8.408203125%
 3: 3.251953125%
 4: 1.259765625%
 5: 0.400390625%
 6: 0.166015625%
 7: 0.087890625%
 8: 0.01953125%
 9: 0.01953125%
 10: 0.009765625%
 13: 0.009765625%

Output Analysis: gamma_variate(1.0, 1.0)
Typical Timing: 63 ± 6 ns
Statistics of 1024 samples:
 Minimum: 0.0002702455969878207
 Median: (0.698793546475219, 0.7042399200830513)
 Maximum: 6.403815315169103
 Mean: 1.0084085455839793
 Std Deviation: 1.0073246802230453
Post-processor distribution of 10240 samples using floor method:
 0: 63.53515625%
 1: 23.02734375%
 2: 8.662109375%
 3: 3.02734375%
 4: 1.19140625%
 5: 0.380859375%
 6: 0.15625%
 7: 0.009765625%
 8: 0.009765625%

Base Case
Output Analysis: Random.weibullvariate(1.0, 1.0)
Typical Timing: 407 ± 14 ns
Statistics of 1024 samples:
 Minimum: 0.0012206653420491654
 Median: (0.6562156146394584, 0.6596006930492667)
 Maximum: 7.040849665771462
 Mean: 1.0019607360886982
 Std Deviation: 1.035819572769456
Post-processor distribution of 10240 samples using floor method:
 0: 62.83203125%
 1: 23.564453125%
 2: 8.2421875%
 3: 3.33984375%
 4: 1.15234375%
 5: 0.556640625%
 6: 0.1953125%
 7: 0.078125%
 8: 0.029296875%
 9: 0.009765625%

Output Analysis: weibull_variate(1.0, 1.0)
Typical Timing: 94 ± 13 ns
Statistics of 1024 samples:
 Minimum: 0.0038869516975269013
 Median: (0.6416038559107055, 0.6435932073838079)
 Maximum: 9.451673963263177
 Mean: 0.9606831278023913
 Std Deviation: 1.008496897342655
Post-processor distribution of 10240 samples using floor method:
 0: 63.7109375%
 1: 22.958984375%
 2: 8.49609375%
 3: 2.919921875%
 4: 1.240234375%
 5: 0.439453125%
 6: 0.1171875%
 7: 0.05859375%
 8: 0.01953125%
 9: 0.0390625%

Output Analysis: extreme_value_variate(0.0, 1.0)
Typical Timing: 63 ± 14 ns
Statistics of 1024 samples:
 Minimum: -2.0420383975334935
 Median: (0.36188771622907123, 0.36486530927718713)
 Maximum: 7.044793427843578
 Mean: 0.5683142371739502
 Std Deviation: 1.3006859382042066
Post-processor distribution of 10240 samples using round method:
 -2: 1.123046875%
 -1: 18.7890625%
 0: 35.146484375%
 1: 25.107421875%
 2: 12.0703125%
 3: 4.951171875%
 4: 1.806640625%
 5: 0.625%
 6: 0.322265625%
 7: 0.029296875%
 8: 0.009765625%
 9: 0.009765625%
 11: 0.009765625%

Base Case
Output Analysis: Random.gauss(5.0, 2.0)
Typical Timing: 625 ± 12 ns
Statistics of 1024 samples:
 Minimum: -1.9044763969904235
 Median: (5.074679905651919, 5.0813395490574145)
 Maximum: 10.902309455122925
 Mean: 5.048020912041488
 Std Deviation: 2.0208474824352933
Post-processor distribution of 10240 samples using round method:
 -3: 0.009765625%
 -2: 0.107421875%
 -1: 0.2734375%
 0: 0.966796875%
 1: 2.919921875%
 2: 6.298828125%
 3: 11.884765625%
 4: 17.28515625%
 5: 20.791015625%
 6: 17.109375%
 7: 12.03125%
 8: 6.4453125%
 9: 2.744140625%
 10: 0.8984375%
 11: 0.1953125%
 12: 0.029296875%
 13: 0.009765625%

Output Analysis: normal_variate(5.0, 2.0)
Typical Timing: 94 ± 8 ns
Statistics of 1024 samples:
 Minimum: -3.6090290281155575
 Median: (4.844783784839538, 4.850649027531264)
 Maximum: 11.006187573326535
 Mean: 4.949982733565797
 Std Deviation: 2.0155669482350604
Post-processor distribution of 10240 samples using round method:
 -4: 0.009765625%
 -3: 0.009765625%
 -2: 0.029296875%
 -1: 0.17578125%
 0: 0.888671875%
 1: 2.8125%
 2: 6.630859375%
 3: 12.802734375%
 4: 17.6171875%
 5: 19.482421875%
 6: 16.9921875%
 7: 11.865234375%
 8: 6.71875%
 9: 2.6953125%
 10: 1.005859375%
 11: 0.205078125%
 12: 0.048828125%
 13: 0.009765625%

Base Case
Output Analysis: Random.lognormvariate(1.6, 0.25)
Typical Timing: 813 ± 41 ns
Statistics of 1024 samples:
 Minimum: 2.338104402040365
 Median: (4.931891345662838, 4.9322410345544645)
 Maximum: 10.39411973225253
 Mean: 5.143022739401719
 Std Deviation: 1.2801179453919909
Post-processor distribution of 10240 samples using round method:
 2: 0.234375%
 3: 8.017578125%
 4: 27.0703125%
 5: 31.572265625%
 6: 18.84765625%
 7: 9.345703125%
 8: 3.359375%
 9: 1.064453125%
 10: 0.37109375%
 11: 0.078125%
 12: 0.0390625%

Output Analysis: lognormal_variate(1.6, 0.25)
Typical Timing: 94 ± 11 ns
Statistics of 1024 samples:
 Minimum: 2.069828319039402
 Median: (4.894080150531378, 4.909775395452343)
 Maximum: 10.529318428639522
 Mean: 5.074098940095621
 Std Deviation: 1.2789688727135649
Post-processor distribution of 10240 samples using round method:
 2: 0.41015625%
 3: 7.880859375%
 4: 27.080078125%
 5: 31.103515625%
 6: 19.853515625%
 7: 9.00390625%
 8: 3.046875%
 9: 1.1328125%
 10: 0.322265625%
 11: 0.126953125%
 12: 0.01953125%
 13: 0.01953125%

Output Analysis: chi_squared_variate(1.0)
Typical Timing: 125 ± 8 ns
Statistics of 1024 samples:
 Minimum: 5.87197856528718e-06
 Median: (0.45153521010163433, 0.45275242065026566)
 Maximum: 12.633198871796893
 Mean: 1.0055263388386824
 Std Deviation: 1.4271720065738391
Post-processor distribution of 10240 samples using floor method:
 0: 67.91015625%
 1: 16.611328125%
 2: 7.158203125%
 3: 3.90625%
 4: 1.845703125%
 5: 1.1328125%
 6: 0.673828125%
 7: 0.302734375%
 8: 0.21484375%
 9: 0.107421875%
 10: 0.0390625%
 11: 0.009765625%
 12: 0.048828125%
 13: 0.01953125%
 16: 0.01953125%

Output Analysis: cauchy_variate(0.0, 1.0)
Typical Timing: 63 ± 10 ns
Statistics of 1024 samples:
 Minimum: -2394.7685394277323
 Median: (-0.03485631278891925, -0.031559860593037996)
 Maximum: 2579.217300653699
 Mean: -1.141710964287314
 Std Deviation: 115.80981938565749
Post-processor distribution of 10240 samples using floor_mod_10 method:
 0: 26.171875%
 1: 11.318359375%
 2: 5.439453125%
 3: 3.8671875%
 4: 3.125%
 5: 3.30078125%
 6: 3.759765625%
 7: 5.546875%
 8: 11.15234375%
 9: 26.318359375%

Output Analysis: fisher_f_variate(8.0, 8.0)
Typical Timing: 188 ± 15 ns
Statistics of 1024 samples:
 Minimum: 0.12718023485213278
 Median: (0.9744413103945309, 0.9762628214097059)
 Maximum: 15.036890310486974
 Mean: 1.2922958439456311
 Std Deviation: 1.2227219395357907
Post-processor distribution of 10240 samples using floor method:
 0: 49.23828125%
 1: 33.173828125%
 2: 10.56640625%
 3: 3.7890625%
 4: 1.50390625%
 5: 0.849609375%
 6: 0.2734375%
 7: 0.244140625%
 8: 0.13671875%
 9: 0.068359375%
 10: 0.05859375%
 11: 0.029296875%
 12: 0.009765625%
 15: 0.009765625%
 16: 0.01953125%
 17: 0.01953125%
 35: 0.009765625%

Output Analysis: student_t_variate(8.0)
Typical Timing: 157 ± 13 ns
Statistics of 1024 samples:
 Minimum: -3.822217211071022
 Median: (-0.03415034496777029, -0.03074096721027831)
 Maximum: 4.635621118946568
 Mean: -0.0037865647333619914
 Std Deviation: 1.133148065978405
Post-processor distribution of 10240 samples using round method:
 -6: 0.01953125%
 -5: 0.0390625%
 -4: 0.302734375%
 -3: 1.552734375%
 -2: 7.1875%
 -1: 22.978515625%
 0: 36.650390625%
 1: 22.734375%
 2: 6.884765625%
 3: 1.30859375%
 4: 0.2734375%
 5: 0.048828125%
 7: 0.01953125%


=========================================================================
Total Test Time: 0.5852 seconds

```
