from functools import wraps
from whatap.trace.trace_context import TraceContext
from whatap.trace.trace_context_manager import TraceContextManager
from whatap.trace.mod.application_wsgi import start_interceptor, end_interceptor, interceptor_step_error
from whatap import logging


def interceptor(fn, task_name, *args, **kwargs):
    ctx = TraceContext()
    ctx.service_name = task_name
    start_interceptor(ctx)
    callback = fn(*args, **kwargs)

    ctx = TraceContextManager.getLocalContext()
    if ctx:
        end_interceptor()
    return callback


def trace_handler(fn, start=False):
    def handler(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ctx = TraceContextManager.getLocalContext()
            if not start and not ctx:
                return fn(*args, **kwargs)
            if ctx and ctx.error_step:
                end_interceptor()
                raise Exception(ctx.error_step)
            try:
                callback = func(*args, **kwargs)
            except Exception as e:
                interceptor_step_error(e)
                ctx = TraceContextManager.getLocalContext()
                if ctx:
                    end_interceptor()
                return fn(*args, **kwargs)
            else:
                return callback
        return wrapper

    return handler

def instrument_celery_execute_trace(module):
    def wrapper(fn, task_name):
        @trace_handler(fn, start=True)
        def trace(*args, **kwargs):
            callback = interceptor(fn, task_name, *args, **kwargs)
            return callback

        return trace
    if hasattr(module, 'build_tracer'):
        _build_tracer = module.build_tracer
        def build_tracer(name, task,*args, **kwargs):
            task = task or module.tasks[name]
            name = ''
            if hasattr(task,'name'):
                name = task.name
            task.run = wrapper(task.run, name)
            return _build_tracer(name, task,*args, **kwargs)

        module.build_tracer = build_tracer