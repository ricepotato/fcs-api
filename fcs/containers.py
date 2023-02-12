import functools


from fcs import repository, config, service


class SingletonInstance:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


class Container(SingletonInstance):
    """의존성 설정 클래스
    하나의 객체만 생성되야 함.
    생성시 Container.instance() 를 사용해야 함."""

    @functools.cached_property
    def settings(self):
        return config.Settings()

    @functools.cached_property
    def repository(self):
        return repository.MongodbRepository(self.settings.mongodb_url)

    def get_fcs_service(self):
        return service.FCSService(self.repository)


container = Container.instance()
