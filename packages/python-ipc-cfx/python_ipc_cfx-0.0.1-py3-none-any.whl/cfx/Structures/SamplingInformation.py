from .base import CFXStructure, is_nullable_number, load_enum
from .SamplingMethod import SamplingMethod


class SamplingInformation(CFXStructure):
    """Describes the sampling strategy to be employed on a particular lot of material / units during test or inspection.

    lot_size (nullable number): The total number of units in the lot
    sample_size (nullable number): The number of units from the total lot to be inspected / tested. This is a subset of the total lot.
    sampling_method (SamplingInformation): An enumeration describing the sampling method that was employed (if any)
    """
    def __init__(self, **kwargs):
        self.lot_size = kwargs.get("lot_size", None)
        if not is_nullable_number(self.lot_size):
            raise TypeError("SamplingInformation: lot_size provided but not a nullable number %s" % self.lot_size)

        self.sample_size = kwargs.get("sample_size", None)
        if not is_nullable_number(self.sample_size):
            raise TypeError("SamplingInformation: sample_size provided but not a nullable number %s" % self.sample_size)

        self.sampling_method = load_enum(kwargs, "sampling_method", SamplingMethod, SamplingMethod.default())
