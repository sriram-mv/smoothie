from functools import wraps
import traceback


from smoothie.exc import CallableCallbackException

class Dispenser(object):

    def __init__(self):
        self.map = {}

    def attach(self, exception=Exception,callback=None):
        def _attach_to_func(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args,**kwargs)

                except exception as ex:
                    if not callable(callback):
                        raise CallableCallbackException
                    else:
                        kwargs['exc_info'] = traceback.format_exc()
                        kwargs['ex'] = ex
                        # HACK(TheSriram): Remove the self arg
                        return callback(args[1:], **kwargs)
            self.map[func.__name__] = func

            return wrapper

        return _attach_to_func

    def original(self, function):
            return self.map[function]

