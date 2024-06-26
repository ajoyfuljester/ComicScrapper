from PySide6 import QtWidgets, QtGui
import ScrapingUtils as SU
from QtUtils import *
import re


class ComicPreview(QtWidgets.QWidget):
    def __init__(self, info):
        super().__init__()


        
        keys = list(info.keys())


        if 'imageURL' in keys or 'image' in keys:
            self.coverLabel = QtWidgets.QLabel()
            self.coverLabel.setAlignment(Alignment.AlignCenter)

            self.coverLabel.setMinimumSize(100, 100)
            self.coverLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding))
            #coverLabel.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Ignored))


            info['image'] = info.get('image') or SU.getImageBytes(info['imageURL'])
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(info['image'])
            self.coverLabel.setPixmap(pixmap)
            if 'imageURL' in keys:
                keys.remove('imageURL')
            if 'image' in keys:
                keys.remove('image')



        self.columnLayout = QtWidgets.QVBoxLayout(self)
        self.columnLayout.addWidget(self.coverLabel)


        d = {}

        for key in keys:
            d[key] = info[key]


        self.description = DescriptionWidget(d)
        self.columnLayout.addWidget(self.description)



    
        
    def resizeCover(self, size):
        pixmap = self.coverLabel.pixmap()
        pixmap = pixmap.scaled(size, KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.coverLabel.setPixmap(pixmap)

        

class DescriptionWidget(QtWidgets.QWidget):
    def __init__(self, entries = {}):
        super().__init__()

        self.formLayout = QtWidgets.QFormLayout(self)
        self.formLayout.setHorizontalSpacing(30)

        linkPattern = re.compile(r'https:\/\/[a-zA-z\d\.]{1,}\/{0,1}')
        
        for k, v in entries.items():
            if linkPattern.match(v):
                v = f'<a href="{v}">{v}</a>'
            valueLabel = QtWidgets.QLabel(v)
            valueLabel.setOpenExternalLinks(True)
            valueLabel.setWordWrap(True)
            valueLabel.setTextInteractionFlags(TextInteractionFlags.TextSelectableByMouse | TextInteractionFlags.LinksAccessibleByMouse | TextInteractionFlags.LinksAccessibleByKeyboard)
            self.formLayout.addRow(k.upper(), valueLabel)

