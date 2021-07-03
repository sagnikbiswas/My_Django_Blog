from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter

def richtext(detail, autoescape=True):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    
    
    #escape html tags
    result = esc(detail)
    """ old code to replace custom tags with HTML tags using a chain of replace methods
    #make texts bold and italic
    result = result.replace("`b`", "<strong>").replace("`/b`", "</strong>").replace("`i`","<em>").replace("`/i`", "</em>")

    #image handling
    result = result.replace("`img`","<img src=\"").replace("`/img`", "\" class=\"img-fluid\"/>")

    #code snippet handling
    result = result.replace("`c`","<pre><code class=\"language-python\">").replace("`/c`","</code></pre>")
    """

    tag_conversion_dict = {
        "`b`": "<strong>",
        "`/b`": "</strong>",
        "`i`": "<em>",
        "`/i`": "</em>",
        "`img`": "<img src=\"",
        "`/img`": "\" class=\"img-fluid\"/>",
        "`c`": "</p><pre><code class=\"language-python\">",
        "`/c`": "</code></pre><p class=\"article-content\">"
    }



    # use these three lines to do the replacement
    tag_conversion_dict = dict((re.escape(k), v) for k, v in tag_conversion_dict.items()) 
    pattern = re.compile("|".join(tag_conversion_dict.keys()))
    result = pattern.sub(lambda m: tag_conversion_dict[re.escape(m.group(0))], result)

    return mark_safe(result)
"""to be done. truncate function for new line characters
@register.filter
@stringfilter
def truncatenewlines(number_of_newlines):
"""
