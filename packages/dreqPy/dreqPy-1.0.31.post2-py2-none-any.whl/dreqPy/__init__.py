
try:
  import packageConfig
  from packageConfig import *
except:
  #from dreqPy import packageConfig
  from .packageConfig import *

try:
  import utilP2
except:
  from dreqPy import utilP2
