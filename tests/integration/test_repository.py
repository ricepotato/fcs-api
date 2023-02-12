import boto3

from fcs import config, models, repository


def test_mongo_repository(settings: config.Settings):

    repo = repository.MongodbRepository(url=settings.mongodb_url)
    repo.delete_all()

    fc = models.FCS(name="FC2PPV-3133751")
    insert_result = repo.insert_fc(fc=fc)
    assert insert_result

    result_fc = repo.get_fc_by_name(name="FC2PPV-3133751")
    assert result_fc.id

    result_fc = repo.get_fc_by_no("3133751")
    assert result_fc.id
