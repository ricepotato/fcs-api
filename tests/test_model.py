from fcs import models


def test_model_fcs_init():
    item = models.FCS(name="ab2-ddv-1234567")
    assert item.no == "1234567"

    fc_dict = item.dict()
    assert fc_dict["status"] == "present"
    fc_dict["_id"] = "1234567"

    parsed_obj = models.FCS.from_mongo_result(fc_dict)
    assert parsed_obj.status == models.Status.present
