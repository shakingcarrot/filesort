from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QLineEdit, QStyle,
    QToolButton, QFileDialog
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Signal, Qt
import pathlib # (추가) pathlib 임포트

class DirectoryBar(QWidget):
    """ 상단 현재 디렉토리 UI 위젯 (기능 추가) """
    
    directory_changed = Signal(str)
    
    def __init__(self): # (수정) default_path 인수 제거
        super().__init__()
        
        # (수정) 현 사용자의 다운로드 폴더를 동적으로 가져옴
        try:
            default_path = str(pathlib.Path.home() / "Downloads")
        except Exception:
            default_path = "C:\\" # 실패 시 C 드라이브
        
        self.setObjectName("DirectoryBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 3, 5, 3)
        
        # Try to load a custom folder icon from workspace; fall back to system icon
        icon_label = QLabel()
        try:
            icon_path = r'D:\\심프랩\\icons8-opened-folder-50.png'
            pix = QPixmap(icon_path)
            if not pix.isNull():
                icon_label.setPixmap(pix.scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                folder_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon)
                icon_label.setPixmap(folder_icon.pixmap(16, 16))
        except Exception:
            folder_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon)
            icon_label.setPixmap(folder_icon.pixmap(16, 16))
        
        dir_label = QLabel('Current Directory')
        
        self.dir_path_edit = QLineEdit(default_path) # (수정) 동적 default_path 적용
        self.dir_path_edit.setObjectName("DirectoryPathEdit")
        
        self.browse_button = QToolButton()
        self.browse_button.setArrowType(Qt.ArrowType.DownArrow)
        self.browse_button.setFixedWidth(25)
        self.browse_button.setObjectName("BrowseButton")
        
        layout.addWidget(icon_label)
        layout.addWidget(dir_label)
        layout.addWidget(self.dir_path_edit)
        layout.addWidget(self.browse_button)
        
        self.browse_button.clicked.connect(self.open_directory_dialog)

    def get_current_path(self):
        """ (추가) 현재 경로 텍스트를 반환하는 함수 """
        return self.dir_path_edit.text()

    def open_directory_dialog(self):
        """ 디렉토리 선택창을 여는 함수 """
        current_path = self.get_current_path()
        
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            current_path
        )
        
        if directory:
            self.dir_path_edit.setText(directory)
            self.directory_changed.emit(directory)