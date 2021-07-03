from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from collections import deque

def tag_unclosed(text):
    
    stack = deque()
    tags = ["c", "i", "b", "img"]
    ptr1, ptr2 = -1, -1

    for i in range(len(text)):
        #print("entering for with token", text[i])
        if text[i] == "`":
            #print("entering first if")
            if ptr1 == -1:
                #print("entering ptr1 if")
                ptr1 = i
            else:
                #print("entering ptr2 if")
                ptr2 = i
                if ptr2 - ptr1 < 2:
                    continue

                tag = text[ptr1+1:ptr2]
                #print(tag, "tag")
                ptr1 = -1

                if tag[0] != "/" and tag in tags:
                    #print("e")
                    stack.append(tag)
                    #print(stack)
                elif tag[0] == "/" and tag[1:] in tags:
                    #print("e")
                    if len(stack) > 0 and stack[-1] == tag[1:]:
                        stack.pop()
                    elif len(stack) == 0:
                        return f"unexpected `{tag}` tag"
                    else:
                        return f"`{stack[-1]}` tag not closed properly!"
                else:
                    #print("else")
                    ptr1 = ptr2
                    ptr2 = -1

    if len(stack) == 0:
        return False
    return f'{", ".join("`"+str(x)+"`" for x in stack)} tag(s) not closed properly!'

def validate_tags(value):
    return_statement = tag_unclosed(value)
    if return_statement:
        raise ValidationError(_(return_statement))

