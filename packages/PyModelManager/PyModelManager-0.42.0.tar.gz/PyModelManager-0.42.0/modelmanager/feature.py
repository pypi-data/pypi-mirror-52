from .model_manager_object import ModelManagerObject


class FeatureRegistry(ModelManagerObject):

    def _use_attributes(self, attributes):
        pass

    def get_features(self):
        status, data = self._requester.request_json_and_check(
            'GET',
            '/features'
        )

        return [
            Feature(self._requester, item)
            for item in data
        ]

    def create_feature(self, name, description):
        payload = {
            'name': name,
            'description': description
        }

        status, data = self._requester.request_json_and_check(
            'POST',
            '/features',
            input=payload
        )

        return self


class Feature(ModelManagerObject):

    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def tags(self):
        return self._tags

    def update(self):
        payload = {
            'name' : self.name,
            'description': self.description,
            'tags': self.tags
        }

        self._requester(
            'PATH',
            '/features/%s' % self.id(),
            input=payload
        )

        return self

    def _use_attributes(self, attributes):
        self._id = attributes['id']
        self._name = attributes['name']
        self._description = attributes['description']
        self._tags = []