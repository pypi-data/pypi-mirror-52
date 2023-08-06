import asyncio
from functools import partial, wraps
from collections import namedtuple, Mapping
from jinja2 import TemplateNotFound, PackageLoader
from sanic.exceptions import ServerError
from sanic.response import HTTPResponse, html
from sanic.views import HTTPMethodView
from sanic_jinja2 import SanicJinja2 as RealSanicJinja2, update_request_context
from spf import SanicPlugin

CONTEXT_PROCESSORS = "context_processor"

SanicJinja2AssociatedTuple = namedtuple('SanicJinja2AssociatedTuple',
                                          ['plugin', 'reg'])


class SanicJinja2Associated(SanicJinja2AssociatedTuple):
    __slots__ = ()

    @property
    def plugin_context(self):
        plugin, reg = self
        spf, name, _prefix = reg
        return spf.get_context(name)

    @property
    def env(self):
        p_context = self.plugin_context
        return p_context.get("jinja_env", None)

    def template(self, template_name, encoding="utf-8", headers=None, status=200):
        """Decorate web-handler to convert returned dict context into
        sanic.response.Response
        filled with template_name template.
        :param template_name: template name.
        :param request: a parameter from web-handler,
                        sanic.request.Request instance.
        :param context: context for rendering.
        """
        plugin = self.plugin
        reg = self.reg
        def wrapper(func):
            nonlocal plugin
            nonlocal reg

            @asyncio.coroutine
            @wraps(func)
            def wrapped(request, *args, **kwargs):
                nonlocal plugin, reg
                nonlocal template_name, encoding, headers, status

                if asyncio.iscoroutinefunction(func):
                    coro = func
                else:
                    coro = asyncio.coroutine(func)

                response = yield from coro(request, *args, **kwargs)

                # wrapped function return HTTPResponse
                # instead of dict-like object
                if isinstance(response, HTTPResponse):
                    return response

                # wrapped function is class method
                # and got `self` as first argument
                if isinstance(request, HTTPMethodView):
                    request = args[0]

                if response is None:
                    response = {}

                context = plugin.get_context_from_spf(reg)
                env = context.get("jinja_env", None)
                if not env:
                    raise ServerError(
                        "Template engine has not been initialized yet.",
                        status_code=500
                    )
                try:
                    template = env.get_template(template_name)
                except TemplateNotFound as e:
                    raise ServerError(
                        "Template '{}' not found".format(template_name),
                        status_code=500
                    )
                if not isinstance(response, Mapping):
                    raise ServerError(
                        "context should be mapping, not {}".format(
                            type(response)
                        ),
                        status_code=500,
                    )
                # if request.get(REQUEST_CONTEXT_KEY):
                #     context = dict(request[REQUEST_CONTEXT_KEY], **context)
                request_context = context.shared.request[id(request)]
                app = context.shared.app
                if 'app' not in request_context:
                    request_context.set('app', app)
                update_request_context(request_context, response)

                if context.get('enable_async', False):
                    text = yield from template.render_async(response)
                else:
                    text = template.render(response)

                content_type = "text/html; charset={}".format(encoding)

                return HTTPResponse(
                    text,
                    status=status,
                    headers=headers,
                    content_type=content_type,
                )

            return wrapped
        return wrapper

    async def render_string_async(self, template, request, **context):
        p_context = self.plugin_context
        env = p_context.get("jinja_env", None)
        request_context = p_context.shared.request[id(request)]
        app = p_context.shared.app
        if 'app' not in request_context:
            request_context.set('app', app)
        update_request_context(request_context, context)
        return await env.get_template(template).render_async(**context)

    async def render_async(
        self, template, request, status=200, headers=None, **context
    ):
        return html(
            await self.render_string_async(template, request, **context),
            status=status,
            headers=headers,
        )

    def render_source(self, source, request, **context):
        p_context = self.plugin_context
        env = p_context.get("jinja_env", None)
        request_context = p_context.shared.request[id(request)]
        app = p_context.shared.app
        if 'app' not in request_context:
            request_context.set('app', app)
        update_request_context(request_context, context)
        return env.from_string(source).render(**context)

    def render_string(self, template, request, **context):
        p_context = self.plugin_context
        env = p_context.get("jinja_env", None)
        request_context = p_context.shared.request[id(request)]
        app = p_context.shared.app
        if 'app' not in request_context:
            request_context.set('app', app)
        update_request_context(request_context, context)
        return env.get_template(template).render(**context)

    def add_env(self, name, obj, scope="globals"):
        env = self.env
        if env:
            if scope == "globals":
                env.globals[name] = obj
            elif scope == "filters":
                env.filters[name] = obj

    def render(self, template, request, status=200, headers=None, **context):
        return html(
            self.render_string(template, request, **context),
            status=status,
            headers=headers,
        )


class SanicJinja2(SanicPlugin):
    __slots__ = tuple()

    AssociatedTuple = SanicJinja2Associated

    def __init__(self, *args, **kwargs):
        super(SanicJinja2, self).__init__(*args, **kwargs)

    @classmethod
    def on_registered(cls, context, reg, *args, **kwargs):
        # this will need to be called more than once,
        # for every app it is registered on.
        app = context.app
        cls.init_app(app, context, *args, **kwargs)

    @classmethod
    def init_app(cls, app, context, *args, loader=None, pkg_name=None,
                 pkg_path=None, context_processors=None, **kwargs):
        log = context.log
        enable_async = kwargs.get("enable_async", False)
        real_sj2 = RealSanicJinja2(app=None,
                                   enable_async=enable_async,
                                   context_processors=context_processors)
        # if context_processors: # What does this even do?
        #     if not hasattr(app, CONTEXT_PROCESSORS):
        #         setattr(app, CONTEXT_PROCESSORS, self.context_processors)
        #         app.request_middleware.append(self.context_processors)

        # Emulate legacy app extension registration
        if not hasattr(app, "extensions"):
            app.extensions = {}

        app.extensions['jinja2'] = real_sj2
        context.jinja2 = real_sj2
        context.jinja_env = real_sj2.env
        context.enable_async = real_sj2.enable_async
        if not loader:
            loader = PackageLoader(
                pkg_name or app.name, pkg_path or "templates"
            )

        real_sj2.env.loader = loader
        real_sj2.add_env("app", app)
        real_sj2.add_env("url_for", app.url_for)
        #real_sj2.url_for = app.url_for


instance = sanic_jinja2 = SanicJinja2()


@sanic_jinja2.middleware(attach_to="request", with_context=True)
async def add_flash_to_request(request, context):
    s_request_context = context.shared.request[id(request)]
    jinja2 = context.jinja2
    if "flash" not in s_request_context:
        s_request_context["flash"] = partial(jinja2._flash, s_request_context)
