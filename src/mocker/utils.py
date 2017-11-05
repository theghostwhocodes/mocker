import os


def compute_file_path(data_path, path, command):
    """Return the computed file path for mocked data

    Keyword arguments:
    data_path -- the path of the folder that contains the subbed data
    path --  the URL path
    command -- the HTTP verb
    """
    return os.path.realpath(
        os.path.join(
            data_path,
            f'{path[1:]}.{command}.json'
        )
    )


def load_mock(file_path):
    """Return the content of the mock file
    """
    with open(file_path, 'rb') as f:
        return f.read()
