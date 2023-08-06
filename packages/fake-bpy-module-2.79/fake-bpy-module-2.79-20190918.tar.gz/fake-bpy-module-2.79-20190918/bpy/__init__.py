import sys
import typing
from . import types
from . import ops
from . import context
from . import path
from . import utils
from . import app
from . import props

context: 'types.Context' = None

data: 'types.BlendData' = None
'''Access to Blenders internal data '''
