'''
EZCSS by diablo

EZCSS is an extra ezhtml module to make it easy to write CSS code.

'''
from ezhtml import *


'''
CSS class string Default Layout
<style>
selector {
	declaration;
	property: value;
}
</style>


These CSS objects can handle multiple selectors
selector0, selector1, selector2 {
	property: value;
}

You can also write external CSS scripts looking like this:



'''


class CSS(Element):

	'''
		CSS (Inherits Element)
			easily make a CSS object that can be appended to your HTML Element!


		CSS( *selectors,  declare=dict() )

		i.e.
		myCSS = CSS( '.myclass', '#id', declare={ 'background-color: 'cyan' } )
		myHtml.appendChild(myCSS)

		myCSS.
	'''


	def __init__(self, *selectors: str, declare=dict()):
		str_declare = str()
		for i in range(len(selectors)):
			str_declare += selectors[i]
			if i != len(selectors)-1:
				str_declare += ', '
		str_declare += ' {'
		for declaration in declare.items():
			str_declare += f'{declaration[0]}: {declaration[1]};\n'
		str_declare += '}'

		Element.__init__(self, 'style', text=str_declare)

		self.__declarations = declare
		self.__selectors = selectors

	@property
	def declarations(self):
		return self.__declarations

	@declarations.setter
	def declarations(self, val:dict()):
		self.__declarations = val

	@property
	def selectors(self):
		return self.__selectors
	
	@selectors.setter
	def selectors(self, *values: str):
		self.__selectors = values

class ExternalCSS(Element):
	def __init__(self, href: str):
		Element.__init__(self, 'link', {
			'rel': 'stylesheet',
			'href': href})
		print(self.attributes)

def write_css(script: CSS):
	pass