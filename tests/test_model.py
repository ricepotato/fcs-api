
from fcs import models

def test_model_fcs_init():
    item = models.FCS(name="ab2-ddv-1234567")
    assert item.no == "1234567"