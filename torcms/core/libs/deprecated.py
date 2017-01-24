import functools
import inspect
import os
import warnings


class _DeprecatedDecorator(object):
    MESSAGE = "%s is @deprecated"

    def __call__(self, symbol):
        if not inspect.isclass(symbol):
            raise TypeError("only classes can be @deprecated")

        warnings.filterwarnings('default',
                                message=self.MESSAGE % r'\w+',
                                category=DeprecationWarning)
        return self._wrap_class(symbol)

    def _wrap_class(self, cls):
        previous_ctor = cls.__init__

        @functools.wraps(previous_ctor)
        def new_ctor(*args, **kwargs):
            self._warn(cls.__name__)
            return previous_ctor(*args, **kwargs)

        cls.__init__ = new_ctor
        return cls

    def _warn(self, name):
        warnings.warn(self.MESSAGE % name, DeprecationWarning,
                      stacklevel=self._compute_stacklevel())

    def _compute_stacklevel(self):
        this_file, _ = os.path.splitext(__file__)
        app_code_dir = self._get_app_code_dir()

        def is_relevant(filename):
            return filename.startswith(app_code_dir) and not \
                filename.startswith(this_file)

        stack = self._get_callstack()
        stack.pop(0)  # omit this function's frame

        frame = None
        try:
            for i, frame in enumerate(stack, 1):
                filename = frame.f_code.co_filename
                if is_relevant(filename):
                    return i
        finally:
            del frame
            del stack

        return 0

    def _get_app_code_dir(self):
        # return ''
        import torcms  # root package for the app
        app_dir = os.path.dirname(torcms.__file__)
        return os.path.join(app_dir, '')  # ensure trailing slash

    def _get_callstack(self):
        frame = inspect.currentframe()
        frame = frame.f_back  # omit this function's frame

        stack = []
        try:
            while frame:
                stack.append(frame)
                frame = frame.f_back
        finally:
            del frame

        return stack

deprecated = _DeprecatedDecorator()
del _DeprecatedDecorator