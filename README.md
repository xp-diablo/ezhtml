# EZHTML

A simple (fun) way to code HTML without coding any HTML!!

### Have you wanted to code a website but HTML looks like gobblygook? 
While there may be more efficient and faster ways to get your site up and looking nice, there are some people (like us) who wish to build a website from the ground-up and work on specific parts of the HTML code. Except... <start-bracket>HTML is suuuuper weird and odd to write with tons of <brackets> everywhere <brackets/> you go!<end-bracket/>

#### That's why...
I wanted to write this project! Given that you are knowledgable in python <sarcastic-facepalm>(🤦)<sarcastic-facepalm/>, and understand basic HTML syntax, you can write your own website and export it as a clean .html file!

---

## How to Use

```
import ezhtml

myHtml = ezhtml.Element('html')

h1 = ezhtml.Element('h1', text='Hello world!')

myHtml.appendChild(h1)

ezhtml.save_html('./page.html', myHtml, html5=True, verbose=True)
# saves file to page.html and prints "Saved html file"
```

#### New!!
I added **ezcss**!!!

##### EZCSS
This is an add on module that makes it easy to write internal and external CSS scripts.

#### How To Use
```
from ezhtml import *
from ezcss import *

myHtml = Element('html')

myInternalScript = CSS('.myclass', '#thisId', {
	'background-color': 'cyan',
	'font-size': '12px'
})

myExternalScript = ExternalCSS('mysheet.css')

myHtml.appendChild(myExternalScript)
myHtml.appendChild(myInternalScript)

save_html('./page.html', myHtml)
# saves file to page.html, does not print output
```