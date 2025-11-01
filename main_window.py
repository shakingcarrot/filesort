from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PySide6.QtCore import Qt

# (수정) DirectoryBar 임포트 제거
from components.files_panel import FilesPanel
from components.log_panel import LogPanel

class MainAppWindow(QWidget):
    """ 메인 애플리케이션 창 (QTabWidget 레이아웃) """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('파일 정리기')
        self.setGeometry(100, 100, 800, 600) 
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. (제거) 상단 패널 (디렉토리 바)
        # self.dir_bar = DirectoryBar() ... (관련 코드 모두 제거)
        
        # 2. 메인 탭 (files / log)
        self.tabs = QTabWidget()
        self.tabs.setObjectName("MainTabs")
        
        # 2-1. Files 탭
        self.files_panel = FilesPanel()
        
        # 2-2. Log 탭
        self.log_panel = LogPanel()
        
        # 탭 추가
        self.tabs.addTab(self.files_panel, 'files')
        self.tabs.addTab(self.log_panel, 'log')
        
        # 3. 메인 레이아웃에 탭 위젯 추가
        main_layout.addWidget(self.tabs)

        # 4. (제거) DirectoryBar 관련 시그널 연결 및 초기 로드 제거
        # self.files_panel.update_directory(...)
        # self.dir_bar.directory_changed.connect(...)