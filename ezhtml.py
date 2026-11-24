'''
EZHTML by diablo

EZHTML is an QOL python module to easily write HTML code without actually writing HTML.
'''

import sys

class TEXT_ORDER:
    '''
        Used for declaring whether the inner text of the html element will be put before or after other sub elements
    '''
    FIRST = True
    LAST  = False

class TAGS:
    VOIDS = (
    "area", "base", "br", "col", "embed", "hr", "img",
    "input", "link", "meta", "source", "track", "wbr")



class Element:
    '''
        A base HTML Element (html, body, div, img, etc.)
    '''

    def __init__(self, tag: str, attr: dict=dict(), text :str=str())-> None:
        self.tag = tag                      # name of the element
        self._attributes = attr             # i.e., src="this.js"
        self.subs = []                  # Sub elements
        self.text_order = TEXT_ORDER.FIRST  # By default, the text inside the element will appear before or after the subs
        self.text = text                    # the inner text inside the element
        self.self_close = True if tag in TAGS.VOIDS else False  # does this element close itself normally? Auto check for us
                                                                # we can change this later if we need
        #for key in self._attributes.keys():             # add the attributes to our class. Make it
        #    setattr(self, key, self._attributes[key])   # easily accessible

    def appendSub(self, sub) -> None:
        '''
            Append a sub elment to the parent.
            (The order you append them in does matter!)
        '''
        for c in self.subs:
            if (c.tag == sub.tag and c._attributes == sub.attributes
                and c.text == sub.text):
                raise ValueError(f"Duplicates <{sub.tag}> has already been appended")
        self.subs.append(sub)
        return sub

    def append(self, sub):    # easier way to type Element.appendSub()
        self.appendSub(sub)

    
    def subTag(self, tag):
        '''
            Grab the sub data from the sub elements
        '''
        out = [c for c in self.subs if c.tag == tag]
        for c in self.subs:
            if hasattr(c, 'subTag'):
                out.extend(c.subTag(tag))
        return out
    
    def searchSubs(self, tag, **attrs):
        '''
            Find a sub element by tags + distiguishing attributes
        '''
        for c in self.subTag(tag):
            if all(c.attributes.get(k) == v for k, v in attrs.items()):
                return c
        return None


    def countSubs(self):
        '''
            Get the count of all the subs inside this html element (and nested subs)
        '''
        ctr = 0
        for sub in self.subs:
            ctr += 1 + sub.countSubs()
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
        setattr(self, var_, val)

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


    def _stringify(self, sub: dict) -> str:
        '''
            Convert this element to a string representation of
            the HTML. This returning string will include sub elements.

            This is a recursive method
            This code is not fomratted to be pretty.
        '''
        ret = str()             # final str
        ret += f'{sub["head"]}'
        closing = sub['self_close']
        if closing:
            return ret


        tag         =   sub['tag']
        text        =   sub['text']
        head        =   sub['head']
        textorder   =   sub['textorder']
        closing     =   sub['self_close']


        if textorder:                       # check if we must put the element text before
            if len(text) >= 1:              # the subs. But ensure we don't write an empty
                ret += text                 # string to the final result

        if len(sub['subs']) >= 1:     # does this element have sub elements?
            for c in sub['subs']:     # if so, start processing the sub elements
                ret += self._stringify(c)

        if not textorder:                   # check if we must put the element text after
            ret += text                     # the subs elements

        ret += f'</{tag}>'                  # close out our element
        return ret

    def __str__(self):
        res = str()
        res += self.head
        subs = []
        for sub in self.subs:
            subs.append(_makeSubTabs(sub, 1))

        for sub in subs:
            res += self._stringify(sub)

        if not self.self_close:
            res += f'</{self.tag}>'

        return res
     # # # # # # # # # # # # # # # # 

    #

    #  End of classes

    #

     # # # # # # # # # # # # # # # #


def _makeSubTabs(element: Element, ctr: int) -> dict:
    '''
        Convert sub elements to dictionaries containing variables which are
        necessary to output to string.

        This is a recursive method.
    '''
    ret = {'tag': element.tag, 'head': element.head, 'tabsize': ctr, 
           'subs': [], 'text': element.text, 'textorder': element.text_order,
           'self_close': element.self_close}

    if element.countSubs() >= 1:
        for sub in element.subs.values():
            ret['subs'].append(_makeSubTabs(sub, ctr+1))
    return ret


def _to_pretty_str(sub: dict):
    '''
            Similar to Element_stringify, but includes formatting to generate
            pretty, easy to read HTML code.

            This is a recursive method.

            Only accessible from the prettify method further below.
    '''

    ret = str()             # final str

    ret += f'\n{"\t"*sub['tabsize']}{sub["head"]}'  # add the entire head of the element

    if sub['self_close']:     # don't worry about the rest of the code if the element is 
                                # self closing
        return ret

    tag         =   sub['tag']
    text        =   sub['text']
    head        =   sub['head']
    textorder   =   sub['textorder']


    if textorder:                       # does the text go before the subs?
        if len(text) >= 1:              # let's make sure the text actually has contents
            ret += text
    if len(sub['subs']) >= 1:     # does this element have sub elements?
        for c in sub['subs']:     # loop through the subs, continue working on the elements
            ret += _to_pretty_str(c)

    if not textorder:                   # check again if the text goes after the the sub Element_stringify
        ret += f'\n{ "\t" * (sub["tabsize"]+1)}{text}'

    if len(sub['subs']) >= 1:     # do we need to indent for sub elements?
        ret += f'\n{"\t" * sub["tabsize"]}'

    # ret += \n\t"*sub["tabsize"]}</{tag}>'
    ret += f'</{tag}>' # close out our element
    return ret

def prettify(html_element: Element, type_='html') -> str:
    '''
        Returns pretty formatted HTML code
    '''
    res = str()
    if type_ == 'html5':            # check if we should add the html5 header
        res += '<!DOCTYPE html>\n'

    res += f'{html_element.head}'           # add our parent element 

    if html_element.text_order and len(html_element.text) >= 1:
        res += str(html_element.text)

    if html_element.countSubs() >= 1:   # then check if we have sub elemenets 
        subs = []
        for sub in html_element.subs:         # loop through our sub elements
            subs.append(_makeSubTabs(sub, 1))    # and make them into parsable data

        for sub in subs:              # begin looping through our parsable data
            res += _to_pretty_str(sub)    # start creating the string values of our subs
    if not html_element.text_order and len(html_element.text) >= 1:
        res += str(html_element.text)
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

