import abc


class HandlerInterface(metaclass=abc.ABCMeta):
    @abc.abstractstaticmethod
    def get_handler():
        """
        Генерация handler-a
        """
        raise NotImplementedError()
