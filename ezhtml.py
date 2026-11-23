'''
EZHTML by diablo

EZHTML is an QOL python module to easily write HTML code without actually writing HTML.
'''

import sys

class TEXT_ORDER:
    '''
        Used for declaring whether the inner text of the html element will be put before or after other child elements
    '''
    FIRST = True
    LAST  = False

class TAGS:
    VOIDS = ('area', 'base', 'br', 'col', 'embed', 'hr', 
             'input', 'img', 'link', 'meta', 'param', 
             'source', 'track', 'wbr')


class Element:
    '''
        A base HTML Element (html, body, div, img, etc.)
    '''

    def __init__(self, tag: str, attr: dict=dict(), text :str=str())-> None:
        self.tag = tag                      # name of the element
        self._attributes = attr             # i.e., src="this.js"
        self.children = {}                  # Child elements
        self.text_order = TEXT_ORDER.FIRST  # By default, the text inside the element will appear before or after the children
        self.text = text                    # the inner text inside the element
        self.self_close = True if tag in TAGS.VOIDS else False  # does this element close itself normally? Auto check for us
                                                                # we can change this later if we need
        for key in self._attributes.keys():             # add the attributes to our class. Make it
            setattr(self, key, self._attributes[key])   # easily accessible

    def appendChild(self, child) -> None:
        '''
            Append a child elment to the parent.
            (The order you append them in does matter!)
        '''

        self.children[child.tag]=child
        setattr(self,child.tag, child)

    def append(self, child):    # easier way to type Element.appendChild()
        self.appendChild(child)


    def countChildren(self):
        '''
            Get the count of all the children inside this html element (and nested children)
        '''
        ctr = 0
        for child in self.children.values():
            ctr += 1 + child.countChildren()
        return ctr

    @property
    def head(self)-> str:
        '''
            Returns the complete head of the HTML element. i.e. '<div id="toast">'
        '''
        r = f"<{self.tag}"
        for attribute in self._attributes.items():
            r += f" {attribute[0]}=\"{attribute[1]}\""
        if self.self_close:
            r += '/'
        r += '>'
        return str(r)

    @property
    def foot(self)->str:
        '''
            Returns the complete foot of the HTML element. i.e. '</div>'
        '''
        return f'</{self.tag}>' if not self.self_close else self.head

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, val: dict):
        self._attributes = val

    def add_attribute(self, var_:str, val:str)-> None:
        '''
            Another method to add attributes.
        '''
        self._attributes[var_] = val
        setattr(self, attr, val)

    def add_attr(self, var_: str, val: str) -> None:
        '''
            An easier way to type Element.add_attribute()
        '''
        self.add_attribute(var_, val)

    def rem_attribute(self, attr_var:str) -> bool:
        '''
            Remove an attribute from this element
        '''
        try:
            del self._attributes[attr_val]
            delattr(self, attr_val)
            return True
        except KeyError:
            return False
    def rem_attr(self, attr_var: str) -> bool:
        '''
            An easier way to type Element.rem_attribute()
        '''
        return self.rem_attribute(attr_var)


    def _stringify(self, child: dict) -> str:
        '''
            Convert this element to a string representation of
            the HTML. This returning string will include child elements.

            This is a recursive method
            This code is not fomratted to be pretty.
        '''
        ret = str()             # final str
        ret += f'{child["head"]}'
        closing = child['self_close']
        if closing:
            return ret


        tag         =   child['tag']
        text        =   child['text']
        head        =   child['head']
        textorder   =   child['textorder']
        closing     =   child['self_close']


        if textorder:                       # check if we must put the element text before
            if len(text) >= 1:              # the children. But ensure we don't write an empty
                ret += text                 # string to the final result

        if len(child['children']) >= 1:     # does this element have child elements?
            for c in child['children']:     # if so, start processing the child elements
                ret += self._stringify(c)

        if not textorder:                   # check if we must put the element text after
            ret += text                     # the children elements

        ret += f'</{tag}>'                  # close out our element
        return ret

    def __str__(self):
        res = str()
        res += self.head
        children = []
        for child in self.children.items():
            children.append(_makeChildTabs(child[1], 1))

        for child in children:
            res += self._stringify(child)

        if not self.self_close:
            res += f'</{self.tag}>'

        return res
     # # # # # # # # # # # # # # # # 

    #

    #  End of classes

    #

     # # # # # # # # # # # # # # # #


def _makeChildTabs(element: Element, ctr: int) -> dict:
    '''
        Convert child elements to dictionaries containing variables which are
        necessary to output to string.

        This is a recursive method.
    '''
    ret = {'tag': element.tag, 'head': element.head, 'tabsize': ctr, 
           'children': [], 'text': element.text, 'textorder': element.text_order,
           'self_close': element.self_close}

    if element.countChildren() >= 1:
        for child in element.children.values():
            ret['children'].append(_makeChildTabs(child, ctr+1))
    return ret


def _to_pretty_str(child: dict):
    '''
            Similar to Element_stringify, but includes formatting to generate
            pretty, easy to read HTML code.

            This is a recursive method.

            Only accessible from the prettify method further below.
    '''

    ret = str()             # final str

    ret += f'\n{"\t"*child['tabsize']}{child["head"]}'  # add the entire head of the element

    if child['self_close']:     # don't worry about the rest of the code if the element is 
                                # self closing
        return ret

    tag         =   child['tag']
    text        =   child['text']
    head        =   child['head']
    textorder   =   child['textorder']


    if textorder:                       # does the text go before the children?
        if len(text) >= 1:              # let's make sure the text actually has contents
            ret += text
    if len(child['children']) >= 1:     # does this element have child elements?
        for c in child['children']:     # loop through the children, continue working on the elements
            ret += _to_pretty_str(c)

    if not textorder:                   # check again if the text goes after the the child Element_stringify
        ret += f'\n{ "\t" * (child["tabsize"]+1)}{text}'

    if len(child['children']) >= 1:     # do we need to indent for child elements?
        ret += f'\n{"\t" * child["tabsize"]}'

    ret += f'\n{"\t"*child["tabsize"]}</{tag}>' # close out our element
    return ret

def prettify(html_element: Element, type_='html5') -> str:
    '''
        Returns pretty formatted HTML code
    '''
    res = str()
    if type_ == 'html5':            # check if we should add the html5 header (enabled by default)
        res += '<!DOCTYPE html>\n'

    res += f'{html_element.head}'           # add our parent element 
    if html_element.countChildren() >= 1:   # then check if we have child elemenets 
        children = []
        for child in html_element.children.items():         # loop through our child elements
            children.append(_makeChildTabs(child[1], 1))    # and make them into parsable data

        for child in children:              # begin looping through our parsable data
            res += _to_pretty_str(child)    # start creating the string values of our children
    if not html_element.self_close:         # double check if our element is self closing
        res += f'\n{html_element.foot}'     # if it isn't we add the foot
    return res



def save_html(path: str, html: Element, html5=True, verbose=False, clean_output=False):

    '''
		Save the HTML element object to a file.

		path            : path to file
		html            : the Element to write
		html5           : Is the document HTML5, or not (OFF by DEFAULT)
		verbose         : Prints when the file finishes saving
        clean_output    : [true]write pretty content, [false] write ugly code
	'''
    with open(path, 'w') as file:
        res = None
        if clean_output:
            res = prettify(html, 'html5')
        else:
            res = str(html)
        file.write(res)
        file.close()
        if verbose:
            print('Saved html file!')

