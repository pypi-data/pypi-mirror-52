from controlpyweb.abstract_reader_writer import AbstractReaderWriter
import threading
from controlpyweb.errors import ControlPyWebReadOnlyError
from str2bool import str2bool


class SingleIO:
    def __init__(self, addr: str = None, *args, **kwargs):
        self.addr = addr
        self.units = kwargs.get("units", "")
        self.name = kwargs.get("name")
        self.namespace = kwargs.get("namespace")
        self._reader_writer = kwargs.get("reader")
        self._default = kwargs.get("default")
        if self._reader_writer is None:
            self._reader_writer = kwargs.get("reader_writer")

    def __and__(self, other):
        if hasattr(other, 'value'):
            return self.value and other.value
        return self.value and other

    def __eq__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value == other

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    def __ne__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value != other

    def __gt__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value > other

    def __lt__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value < other

    def __ge__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value >= other

    def __le__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value <= other

    def __get__(self, instance, owner):
        self.read()
        return self

    def __set__(self, obj, value):
        raise ControlPyWebReadOnlyError

    def __str__(self):
        return f'[{type(self).__name__}] {self.name} = {self.value}'

    def __add__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value + other

    def __sub__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value - other

    def __mul__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value * other

    def __truediv__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value / other

    def __floordiv__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value // other

    @property
    def value(self):
        val = self.read()
        if val is None:
            return self._default
        return self._convert_type(val)

    @staticmethod
    def _convert_type(value):
        return value

    def read(self):
        if self._reader_writer is None:
            return None
        val = self._reader_writer.read(self.addr)
        val = self._convert_type(val)
        return val

    def read_immediate(self):
        val = self._reader_writer.read_immediate(self.addr)
        return val









