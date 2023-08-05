


from jk_hwriter import HWriter

from .HElement_HAbstractElementList import *




class HToolkit_Write_PlainText(object):

	@staticmethod
	def __addPlainTextSimple(e:HElement, w:HWriter):
		for ea in e.children:
			if isinstance(ea, HText):
				w.writeLn(ea.text)
			elif isinstance(ea, HElement):
				HToolkit_Write_PlainText.__addPlainTextSimple(ea, w)
	#

	@staticmethod
	def writePlainText(root:HElement, w:HWriter):
		assert isinstance(root, HElement)
		assert isinstance(w, HWriter)

		HToolkit_Write_PlainText.__addPlainTextSimple(root, w)
	#

#










