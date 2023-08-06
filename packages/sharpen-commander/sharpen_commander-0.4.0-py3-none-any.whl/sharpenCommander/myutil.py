
from .urwidHelper import *

def unwrapQutesFilename(ss):
	if ss.startswith('"'):
		# escape including qutes
		ss = ss[1:-1].replace('"', '\\"')
		return ss
	else:
		return ss

"""
itemList = list of (markup,  attr)
"""
def refreshBtnListMarkupTuple(markupItemList, listBox, onClick):
	#listBox.itemCount = len(markupItemList)
	#if listBox.itemCount == 0:
	if len(markupItemList) == 0:
		markupItemList = [("std", "< Nothing > ", None)]

	del listBox.body[:]
	listBox.body += btnListMakeMarkup(markupItemList, onClick)

"""
itemList = list of (terminal, attr)
"""
def refreshBtnListTerminal(terimalItemList, listBox, onClick):
	#listBox.itemCount = 
	#if listBox.itemCount == 0:
	if len(terimalItemList) == 0:
		terimalItemList = [("< Nothing > ", None)]

	del listBox.body[:]
	listBox.body += btnListMakeTerminal(terimalItemList, onClick)


def fileBtnName(btn):
	label = btn.original_widget.get_label()
	return label.strip()


def gitFileBtnName(btn):
	label = btn.original_widget.get_label()
	return label[2:].strip()

# "??" - untracked file
def gitFileBtnType(btn):
	label = btn.original_widget.get_label()
	return label[:2]


def gitFileLastName(btn):
	ftype = gitFileBtnType(btn)
	fname = gitFileBtnName(btn)
	#R  b -> d
	#R  "test a.txt" -> "t sp"
	#A  "test b.txt"
	#A  "tt \"k\" tt"
	if not ftype.startswith("R"):
		return unwrapQutesFilename(fname)

	# case1. a -> b
	if not fname.startswith("\""):
		pt = fname.rindex(" -> ")
		fname = fname[pt+4:]
		return unwrapQutesFilename(fname)
	else:
		# case2. "test a" -> "test b"
		ss = fname[:-1]
		while True:
			pt = ss.rfind('"')
			if pt == 0:
				return ss[1:]

			if pt != -1:
				if ss[pt-1] != "\\":
					return ss[pt+1:]
				else:
					# TODO:
					raise Exception("Not supported file format[%s]" % fname)

