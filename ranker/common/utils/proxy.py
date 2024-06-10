from functools import cached_property


class LazyProxy:
    def __init__(self, obj_creator: callable):
        self.create_obj = obj_creator

    @cached_property
    def _target_obj(self):
        return self.create_obj()

    def __call__(self, **kargs):
        return self._target_obj(**kargs)

    def __getattr__(self, name: str):
        return getattr(self._target_obj, name)
