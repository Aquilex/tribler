from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget


class ChannelListItem(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        uic.loadUi('qt_resources/channel_list_item.ui', self)

        self.channel_thumbnail.setPixmap(QPixmap("images/default-placeholder.png"))