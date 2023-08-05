


import os
import sys

from jk_hwriter import HWriter

from .HAbstractElement import HAbstractElement
from .HAttribute import HAttribute
from .HAttributeList import HAttributeList
from .HText import HText
from .HElement_HAbstractElementList import HElement, HAbstractElementList



class HToolkit_Write_Dump(object):

	@staticmethod
	def __writeAttribute(a:HAttribute, w:HWriter):
		if a.value:
			w.writeLn("--- " + a.name + "=" + HToolkit_Write_Dump.__toText(a.value))
		else:
			w.writeLn("--- " + a.name)
	#

	@staticmethod
	def __writeHElement(e:HElement, w:HWriter):
		w.writeLn("<<<" + e.name + ">>>")

		if e.attributes:
			w.incrementIndent()
			for a in sorted(e.attributes, key=lambda x: x.name):
				HToolkit_Write_Dump.__writeAttribute(a, w)
			w.decrementIndent()

		if e.children:
			w.incrementIndent()
			for ea in e.children:
				if isinstance(ea, HText):
					w.writeLn(HToolkit_Write_Dump.__toText(ea.text))
				elif isinstance(ea, HElement):
					HToolkit_Write_Dump.__writeHElement(ea, w)
			w.decrementIndent()
	#

	@staticmethod
	def writeDump(root:HElement, w:HWriter):
		assert isinstance(root, HElement)
		assert isinstance(w, HWriter)

		HToolkit_Write_Dump.__writeHElement(root, w)
	#

	@staticmethod
	def __toText(s:str):
		s = repr(s)
		return "\"" + s[1:-1] + "\""
	#

#













