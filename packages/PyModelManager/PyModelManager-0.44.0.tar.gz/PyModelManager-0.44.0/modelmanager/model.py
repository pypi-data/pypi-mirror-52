from .model_manager_object import ModelManagerObject


class Model(ModelManagerObject):

    @property
    def author(self):
        return self._author

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def algorithm(self):
        return self._algorithm

    @property
    def characteristics(self):
        return self._characteristics

    @property
    def features(self):
        return self._features

    @property
    def label(self):
        return self._label

    def _use_attributes(self, attributes):
        self._author = attributes['author']
        self._name = attributes['name']
        self._title = attributes['title']
        self._description = attributes['description']
        self._algorithm = attributes['algorithm']
        self._characteristics = attributes['characteristics']
        self._features = attributes['features']
        self._label = attributes['label']

