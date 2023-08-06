from typing import Any, AnyStr, Dict, List, Union


def read(path: Union[str, bytes, int], extension: str, **kwargs: Any) -> Union[AnyStr, List[AnyStr]]:
    """
    Wrapper for various methods to read data from a file

    :param path: file's path.
    :param extension: files format.
    available formats are:
    - "text"
    - "json"
    - "pickle"
    :param kwargs dictionary of other options.
    available options are:
    -
    :return: content of file
    """

    if extension == "text":
        return text_reader(path, **kwargs)


def text_reader(path: Union[str, bytes, int], **kwargs: Any) -> Union[AnyStr, List[AnyStr]]:
    """ Reads in all of a textual file """

    # default settings
    config: Dict[str, Any] = dict(encoding="utf-8", readlines=False, max_length=-1, max_lines=None,
                                  line_step=1)

    # modify settings with user provided values in kwargs
    for key in config.keys():
        if key in kwargs:
            config[key] = kwargs[key]

    with open(path, 'r', encoding=config["encoding"]) as file:
        if config["readlines"]:
            data = file.readlines(config["max_length"])
            if config["max_lines"]:
                data = [data[line] for line in range(0, config["max_lines"], config["line_step"])]
            elif config["line_step"] != 1:
                data = [data[line] for line in range(0, len(data), config["line_step"])]
        else:
            data = file.read(config["max_length"])
    return data
