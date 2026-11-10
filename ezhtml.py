'''
EZHTML by diablo

EZHTML is an easy-to-use python module to write HTML code without actually writing HTML.
'''

import sys

class TEXT_ORDER:
	'''
		Used for declaring whether the inner text of the HTML element will be put before or after other children elements.
	'''
	FIRST = True
	LAST = False


class Element:
	'''
		An HTML Element (html, body, div, img, etc.)
	'''

	def __init__(self, tag_: str, attr=dict(), text=str()):

		self.__tag = tag_               # <html> <div> <img> <href>...
		self.__Attributes = attr        # src=""
		self.__children = {}            # <html><div tag="child"></div></html>
		self.__text_order = True        # <div>Before<child/></div> <div><child/>After</div>
		self.__text = text              # <div> My Text Here </div>

		# make the attributes for the html tag be an acual part of the element, rather than "myElement.attribute['id'] = blahblahblah"
		for key in self.__Attributes.keys():
			setattr(self, key, self.__Attributes[key])
    
	def appendChild(self, child):
		'''
			Append a child element object to this element
		'''
		self.__children[child.tag]=child
		setattr(self, child.tag, child)

	def childrenCount(self):
		'''
			Get the count of all the children inside this html element (and nested children)
		'''

		ctr = 0
		for child in self.__children.values():
			ctr += 1 + child.childrenCount()
		return ctr

	@property
	def head(self):
		'''
			The HTML tag head; i.e. '<div id="bruh">'
		
		'''
		r = f'<{self.tag}'
		for attribute in self.__Attributes.items():
			r += f' {attribute[0]}="{attribute[1]}"'
		return r + '>'

	@property
	def foot(self):
		'''
			The HTML tag foot; i.e. '</div>'
		'''
		return f'</{self.tag}>'

	@property
	def children(self):
		'''
			Get the list of children this element has (Non-recursive)
		'''
		return self.__children

	@property
	def tag(self):
		'''
			The element's tag; i.e. "head", "div", "id"
		'''
		return self.__tag

	@tag.setter
	def tag(self, val: str):
		self.__tag = val

	@property
	def text(self):
		return self.__text

	@text.setter
	def text(self, val: str):
		self.__text = val

	@property
	def text_order(self):
		'''
			The order which the text should be in.
			The text should be BEFORE any children, or AFTER any child elements.
		'''
		return self.__text_order

	@text_order.setter
	def text_order(self, val: bool):
		self.__text_order = val

	@property
	def attributes(self):
		'''
			Returns the dictionary containing all the attributes to this element.
		'''
		return self.__Attributes

	@attributes.setter
	def attributes(self, val: dict):
		if type(val) != dict:
			print('Must set attributes to a dict...')
			raise Exception()
		else:
			self.__Attributes = val

	def add_attr(self, attr:str, val: str)-> None:
		'''
			Add an attribute to this element
		'''
		self.__Attributes[attr] = val
		setattr(self, attr, val)

	def rem_attr(self, attr: str) -> bool:
		'''
			Remove an attribute from this element
		'''

		# should an error occur (maybe the attribute doesn't exist?), will return False
		try:
			del self.__Attributes[attr]
			delattr(self, attr)
			return True
		except KeyError:
			return False

	def __str__(self):
		return prettify(self)

	def __repr__(self):
		return f'Element: {self.tag}; {self.childrenCount()} child(ren)'


	# # # # # # # #
	#
	#
	# END OF CLASS
	#
	#
	# # # # # # # #

def _r_html_blocks_to_str(child: dict) -> str:
	'''
		Output the text of the children elements and the parent element.

		Recursive method
	'''
	ret = str() 					# final output string
	tag = child['tag']				# element tag
	text = child['text']			# inner text
	head = child['head']			# head of the elmement
	tabsize = child['tabsize']		# size of tabs
	textorder = child['textorder']	# order of the inner text

	ret += f'\n{'\t'*tabsize}{head}' # add a new line, tab out the text and place the new element

	if textorder:					# text goes before the children
		if len(text) > 1:			# check if the text has a value/isn't empty
			ret += child['text']

	if len(child['children']) >= 1:				# does this element have children elements?
		for c in child['children']:				# iterate through each child element
			ret += _r_html_blocks_to_str(c)

	if not textorder:		# < ==  ==  ==  ==  	# the text is after the child element 
		if len(text) > 1:							# the inner text is not empty
			ret += f'\n{ "\t" * (tabsize+1)}{text}'

	if not len(child['children']) >= 1:
		ret += f'</{tag}>' if notSelfClosing(Element(tag)) else ''
	else:
		ret += f'\n{"\t"*tabsize}</{tag}>' if notSelfClosing(Element(head)) else ''

	return ret		# output the final string

def _r_html_child_tabs_text(element: Element, ctr: int)-> dict:
	# get the formatted information for each html element and child
	ret = { 'tag': element.tag, 'head': element.head, 'tabsize': ctr, 'children': [], 'text': element.text, 'textorder': element.text_order }
	
	# if there are any children, append any other children objects
	if element.childrenCount() >= 1:
		for child in element.children.values():
			ret['children'].append(_r_html_child_tabs_text(child, ctr + 1))
	return ret

def notSelfClosing(element: Element) -> bool: # returns True if the element is not in the list
	return not element.tag in ('img', 'br', 'hr', 'input', 'meta', 'link') # returns false if it is in the list


def prettify(html_element: Element, type_='html') -> str:
	'''
		Returns a pretty formatted HTML code
	'''

	res = str() # final result string

	if type_ == 'html5':				# check if we want to write the html5 header
		res += '<!DOCTYPE html>\n'		# write it so

	res += f'{html_element.head}'			# add the head of the html element
	if html_element.childrenCount() >= 1:	# if there is a child element....
		children = []
		for child in html_element.children.items():		# loop through the child elements...
			children.append(_r_html_child_tabs_text(child[1], 1))	# begin adding the string of the child element to our list

		for child in children:						# begin iterating though our strings
			res += _r_html_blocks_to_str(child)		# add the formatted text of the element to our resulting string

	res += f'\n{html_element.foot}' if notSelfClosing(html_element) else '' #add the foot 
	return res		# return our resulting string



def save_html(path: str, html: Element, html5=True, verbose=False):
	'''
		Save the HTML element object to a file.

		path    : path to file
		html    : the Element to write
		html5   : Is the document HTML5, or not (OFF by DEFAULT)
		verbose : Prints when the file finishes saving
	'''
	with open(path, 'w') as file:
		res = None
		if html5:		# we require the html5 header
			res = prettify(html, 'html5')
		else:			# we do not require the html5 header
			res = prettify(html)

		file.write(res)
		file.close()
		if verbose:
			print("Saved html file")