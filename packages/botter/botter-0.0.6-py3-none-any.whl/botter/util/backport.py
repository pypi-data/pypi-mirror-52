try:
    from typing import NoReturn
except ImportError:
    class NoReturn:
        """
        Special type indicating functions that never return.
        Example::
    
          from typing import NoReturn
    
          def stop() -> NoReturn:
              raise Exception('no way')
    
        This type is invalid in other positions, e.g., ``List[NoReturn]``
        will fail in static type checkers.
        """
        
        pass

__all__ = \
[
    'NoReturn',
]
