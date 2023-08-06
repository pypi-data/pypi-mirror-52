import os

def safe_remove(f: str):
    """
    Removes the file safely, checking for its existence
    and ignoring any errors.
    Used in cleanup methods.
    
    :param f: str
    """
    if (os.path.isfile(f)):
        try:
            os.remove(f)
        except OSError:
            pass

__all__ = \
[
    'safe_remove',
]
