from typing import Dict, Optional, Any, Callable


class ClassRegistry(Dict[str, Callable]):

    def check_key(self, key: str) -> None:
        pass

    def check_value(self, value: Callable) -> None:
        pass

    def check(self, key: str, value: Callable) -> None:
        try:
            self.check_key(key)
        except KeyError:
            raise
        except Exception as e:
            raise KeyError(str(e))

        try:
            self.check_value(value)
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(str(e))

    def register(self, key: str, value: Callable) -> None:
        self[key] = value

    def unregister(self, key: str) -> None:
        del self[key]

    def __setitem__(self, key: str, value: Callable) -> None:
        self.check(key, value)
        super().__setitem__(key, value)

    @property
    def metaclass(self) -> type:
        class RegistryMetaclass(type):

            def __new__(cls,
                        name: str,
                        *args: Any,
                        register: bool = True,
                        key: Optional[str] = None,
                        **kwargs: Any) -> type:
                newclass = super().__new__(cls, name, *args, **kwargs)
                if register:
                    self.register(key or name, newclass)
                return newclass

        return RegistryMetaclass
