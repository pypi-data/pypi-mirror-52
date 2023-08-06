from typing import Any, Dict, Tuple

from torch import Tensor

from .activations import ActivationName

DataDict = Dict[str, Tensor]
ResultsDict = Dict[ActivationName, Dict[str, Any]]

LinearDecoder = Tuple[Tensor, Tensor]
