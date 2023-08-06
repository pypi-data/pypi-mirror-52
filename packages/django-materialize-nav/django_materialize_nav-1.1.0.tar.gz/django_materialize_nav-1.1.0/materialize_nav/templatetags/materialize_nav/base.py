from django import template
from django.template.base import FilterExpression, kwarg_re
from django.urls import resolve, Resolver404, reverse_lazy
from django.utils.safestring import mark_safe

__all__ = ["register"]


register = template.Library()


def parse_args_kwargs(parser, bits):
    # Parse the rest of the args, and build FilterExpressions from them so that
    # we can evaluate them later.
    args = []
    kwargs = {}
    for bit in bits:
        # Is this a kwarg or an arg?
        match = kwarg_re.match(bit)
        kwarg_format = match and match.group(1)
        if kwarg_format:
            key, value = match.groups()
            kwargs[key] = FilterExpression(value, parser)
        else:
            args.append(FilterExpression(bit, parser))
    return args, kwargs


@register.tag(name="wrap_href")
def do_href_if_exists(parser, token):
    # Split the tag content into words, respecting quoted strings.
    tag_name, *bits = token.split_contents()
    if len(bits) < 1:
        raise template.TemplateSyntaxError("Path argument is required")

    args, kwargs = parse_args_kwargs(parser, bits)

    nodelist = parser.parse(('endwrap_href',))
    parser.delete_first_token()
    return HrefIfExists(nodelist, *args, **kwargs)


class HrefIfExists(template.Node):
    def __init__(self,  nodelist, path=None, class_names='', style=''):
        self.nodelist = nodelist
        self.path = path
        self.class_names = class_names
        self.style = style

    def render(self, context):
        path = self.path
        if path:
            path = self.path.resolve(context)

        class_names = self.class_names
        if class_names:
            class_names = self.class_names.resolve(context)

        style = self.style
        if style:
            style = self.style.resolve(context)

        content = self.nodelist.render(context)
        if link_exists(path):
            a_tag = mark_safe('<a href="{}" class="{}" style="{}">'.format(get_link(path), class_names, style))
            end_a_tag = mark_safe('</a>')
            return a_tag + content + end_a_tag
        return content


def link_exists(path):
    """Returns True for successful resolves()'s."""
    try:
        return bool(resolve(path))
    except Resolver404:
        return False


def get_link(path):
    try:
        return str(reverse_lazy(path))
    except:
        return str(path)
