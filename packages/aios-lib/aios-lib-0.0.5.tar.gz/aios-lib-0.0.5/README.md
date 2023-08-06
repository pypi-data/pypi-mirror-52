## AIOS LIB

Library for AIOS program

#### Build

~~~python
python3 setup.py sdist bdist_wheel
~~~

#### Intallation

~~~shell
pip3 install wheel_file_path
~~~

#### Usage

~~~python
from aios-lib.utils import *

# Obtain data directory from environment variables
data_dir = get_data_dir()
# Obtain model directory from environment variables
model_dir = get_model_dir()
# Report model score to clustar aios server
score = 1
report_score(score)
~~~

#### Acknowledge
