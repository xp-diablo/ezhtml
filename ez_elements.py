'''

    A compliation of preset elements easy to write.

'''


from ezhtml import Element, TAGS, TEXT_ORDER, prettify



class Break(Element):
    def __init__(self):
        super().__init__('br')

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, val):
        if hasattr(self, '_tag'):
            raise AttributeError('tag is read-only')
        self._tag = val


class Embed(Element):
    def __init__(self, embed_type: str, src:str = str(), attrs:dict = dict()):
        super().__init__('embed')
        self._embedded = src

        match embed_type:
            case "pdf" | "application/pdf":
                self.add_attr('src', src)
                self.add_attr('type', 'application/pdf')
            
            case "image" | "img" | "photo":
                self.tag = 'img'
                self.add_attr('src', src)
                self.add_attr('alt', str())
            
            case "audio" | "music":
                self.tag = 'audio controls'
                self.add_attr('src', src)
            
            case "video":
                self.tag = 'video controls'
                self.add_attr('src', src)

            case "iframe":
                self.tag = 'iframe'
                self.add_attr('src', src)

            case "object":
                self.tag = "object"
                self.add_attr('data', src)
                self.add_attr('type', 'media/type')

        self.attributes = self.attributes | attrs


# Heading Text Classes

class H1(Element):
    def __init__(self, text:str = str(), attributes:dict = dict()):
        super().__init__('h1', attributes, text)

class H2(Element):
    def __init__(self, text: str = str(), attributes:dict = dict()):
        super().__init__('h2', attributes, text)

class H3(Element):
    def __init__(self, text: str = str(), attributes:dict = dict()):
        super().__init__('h3', attributes, text)

class H4(Element):
    def __init__(self, text:str = str(), attributes:dict = dict()):
        super().__init__('h4', attributes, text)

class H5(Element):
    def __init__(self, text:str = str(), attributes:dict = dict()):
        super().__init__('h5', attributes, text)


class InputField(Element):
    def __init__(self, prompt: str = str(), attributes: dict= dict(), input_type:str = 'text'):
        super().__init__('input', {'type': input_type, 
                                   'placeholder': prompt} | attributes)

        self._prompt = self.text
        self._input_type = 'text' # default input field is a text field
        self.add_attr('type', self._input_type)

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, val: str):
        self._prompt = val
        self.attributes['placeholder']=val

    @property
    def input_type(self):
        return self._input_type

    @input_type.setter
    def input_type(self, val):
        self._input_type = val
        self.attributes['type']=self._input_type
