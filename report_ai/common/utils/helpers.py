import json
import time
import yaml
import msgpack
from box import Box
from typing import List
from functools import reduce, wraps
from importlib.metadata import version

__all__ = ["MissingEnvironmentVariable", "load_yaml_file", "retry", "serializer", "chunker", "Singleton",
           "validate_package_version"]


class MissingEnvironmentVariable(Exception):
    pass


# helper functions and classes
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ObjectSerializer:
    """
    Custom Class to serialize or deserialize objects
    """

    @staticmethod
    def serialize(obj, serializer: str = None):
        if serializer == 'json':
            obj = json.dumps(obj, default=str)
        elif serializer == 'msgpack':
            obj = msgpack.packb(obj)
        return obj

    @staticmethod
    def deserialize(obj, serializer: str = None):
        if serializer == 'json':
            obj = json.loads(obj)
        elif serializer == 'msgpack':
            obj = msgpack.unpackb(obj)
        return obj


def load_yaml_file(file_name):
    """
    function to load yaml file to Box object
    """
    return Box.from_yaml(filename=file_name, Loader=yaml.FullLoader)


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None, default_return_value=None):
    """Retry calling the decorated function using an exponential backoff.

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    :param default_return_value: default value to return by decorated function if it fails on last try
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            try:
                return f(*args, **kwargs)
            except Exception:
                if logger:
                    logger.exception(f"error in func: {f.__name__} ")
                return default_return_value

        return f_retry  # true decorator

    return deco_retry


def chunker(l: List, n: int):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_installed_version(package_name):
    try:
        return version(package_name)
    except ModuleNotFoundError:
        return None


def validate_package_version(package_name, required_version):
    installed_version = get_installed_version(package_name)

    if installed_version != required_version:
        raise Exception(
            f'Invalid version of {package_name} installed. '
            f'Expected: {required_version}, found: {installed_version if installed_version is not None else "None"}')


serializer = ObjectSerializer()
