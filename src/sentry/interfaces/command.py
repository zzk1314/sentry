from __future__ import absolute_import

__all__ = ('Command',)

from sentry.interfaces.base import Interface, InterfaceValidationError
from sentry.utils.safe import trim


class Command(Interface):
    """
    An interface which describes commands.

    >>> {
    >>>     "executable": "/usr/bin/ls",
    >>>     "args": ["-alh", "/"],
    >>>     "exit_code": 0
    >>> }
    """
    @classmethod
    def to_python(cls, data):
        args = []
        for arg in data.get('args') or ():
            args.append(trim(arg, 4096))
        if data.get('exit_code') is not None:
            try:
                exit_code = int(data['exit_code'])
            except (ValueError, TypeError):
                raise InterfaceValidationError('Invalid exit code')
        else:
            exit_code = None

        return cls(
            executable=trim(data.get('executable'), 255),
            args=args,
            exit_code=exit_code,
            output=trim(data.get('output'), 65000),
            env=trim(data.get('environ') or {}),
        )

    def get_api_context(self, is_public=False):
        return {
            'executable': self.executable,
            'args': self.args,
            'exitCode': self.exit_code,
            'output': self.output,
            'env': self.env,
        }

    def get_path(self):
        return 'sentry.interfaces.Command'

    def get_hash(self):
        return []
