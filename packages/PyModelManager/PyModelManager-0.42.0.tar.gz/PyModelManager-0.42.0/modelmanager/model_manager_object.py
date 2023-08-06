class ModelManagerObject(object):
    def __init__(self, requester, attributes=None) -> None:
        super().__init__()

        self._requester = requester
        self._use_attributes(attributes)

    def update(self):
        pass

    def _use_attributes(self, attributes):
        pass