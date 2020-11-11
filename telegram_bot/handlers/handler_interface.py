import abc


class HandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_handler(self):
        """
        Генерация handler-a
        """
        raise NotImplementedError()
