from .model_manager_object import ModelManagerObject
from .model import Model


class Project(ModelManagerObject):

    def get_models(self):
        status, data = self._requester.request_json_and_check(
            'GET',
            '/models'
        )

        return [
            Model(self._requester, item)
            for item in data
        ]

    def get_model(self, id=None):
        return None

    def _use_attributes(self, attributes):
        pass

