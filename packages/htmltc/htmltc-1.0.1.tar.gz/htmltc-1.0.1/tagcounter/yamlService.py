import yaml
import os


def get_value_by_key(key):
    with touchopen('domains.yaml', 'r+') as yaml_file:
        data = yaml.load(yaml_file)
        if data is not None:
            if data.keys().__contains__(key):
                return data[key]


def add_value(key, value):
    with open('domains.yaml', 'w') as yaml_file:
        yaml.dump({key: value}, yaml_file)


def touchopen(filename, *args, **kwargs):
    # Open the file in R/W and create if it doesn't exist. *Don't* pass O_TRUNC
    fd = os.open(filename, os.O_RDWR | os.O_CREAT)

    # Encapsulate the low-level file descriptor in a python file object
    return os.fdopen(fd, *args, **kwargs)
