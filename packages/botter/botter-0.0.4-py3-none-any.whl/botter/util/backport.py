try:
    from typing import NoReturn
except ImportError:
    from typing import _SpecialForm

    # noinspection PyArgumentList
    NoReturn = _SpecialForm('NoReturn', doc=
    """Special type indicating functions that never return.
    Example::

      from typing import NoReturn

      def stop() -> NoReturn:
          raise Exception('no way')

    This type is invalid in other positions, e.g., ``List[NoReturn]``
    will fail in static type checkers.
    """)
    del _SpecialForm

__all__ = \
[
    'NoReturn',
]
