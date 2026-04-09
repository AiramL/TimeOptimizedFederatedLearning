from .oracle import ServerOracleTOFLSelection
from .m_fastest import ServerMFastestSelection
from .random import ServerRandomSelection

from .fixed import (
    ServerFixedSelection,
    ServerFixedTestSelection
)

from .tofl import ServerTOFLSelection

from .tofl_selection_dl import ServerEstimatorTOFLSelectionDL

from .tofl_mfastest import (
    ServerEstimatorTOFLSelectionMFastestClients,
    ServerEstimatorTOFLSelectionMFastest,
)