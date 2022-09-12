import argparse


class StoreDictKeyPair(argparse.Action):
    def __init__(self, *args, **kwargs):
        super(StoreDictKeyPair, self).__init__(*args, **kwargs)
        self._parsed_values = {}

    def __call__(self, parser, namespace, values, option_string=None):
        for value in values:
            splitted_key_value = value.split("=")
            if len(splitted_key_value) != 2:
                raise ValueError(
                    f"Key-Value pairs have to be supplied in key=value format, was '{value}'"
                )
            k, v = splitted_key_value
            self._parsed_values[k] = v
        setattr(namespace, self.dest, self._parsed_values)
