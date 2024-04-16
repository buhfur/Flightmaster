self.scrollBar.setParent(self.searchAddonsTab) : makes the scrollbar  widget not show up


self.scrollBar.resize(self.searchAddonsTab.sizeHint()) : makes the scrollbar a tiny box in the top left corner 



self.searchAddonsLayout.addWidget(self.scrollBar)  : for some reaso this fixed the weird layout issue  I was having with the window covering other widgets in other layouts
