from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, 
    QTreeWidgetItem, QPushButton, QHeaderView, QLabel, QSplitter
)
from PySide6.QtCore import Slot, Qt

class LogPanel(QWidget):
    """ 'log' 탭 (좌우 분할 로그 뷰어) """
    
    def __init__(self):
        super().__init__()
        self.setObjectName("LogPanel")
        
        # 1. 메인 레이아웃 (QVBoxLayout)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
        # 2. 좌우 분할 QSplitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setObjectName("LogPanelSplitter")
        
        # 2-1. 왼쪽 (로그 제목 목록)
        self.log_titles_tree = QTreeWidget()
        self.log_titles_tree.setObjectName("LogTitlesTree")
        self.log_titles_tree.setHeaderLabels(["정리 로그"])
        
        # 2-2. 오른쪽 (로그 상세 내용)
        log_details_widget = QWidget()
        log_details_layout = QVBoxLayout(log_details_widget)
        log_details_layout.setContentsMargins(0, 0, 0, 0)
        
        self.log_details_label = QLabel("로그 제목을 선택하세요") # 초기 라벨
        self.log_details_label.setObjectName("LogDetailsLabel")
        
        self.log_details_tree = QTreeWidget()
        self.log_details_tree.setObjectName("LogDetailsTree")
        self.log_details_tree.setHeaderLabels(['번호', '파일', '이동 경로'])
        self.log_details_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.log_details_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.log_details_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        log_details_layout.addWidget(self.log_details_label)
        log_details_layout.addWidget(self.log_details_tree)

        # 3. 스플리터에 추가
        self.splitter.addWidget(self.log_titles_tree)
        self.splitter.addWidget(log_details_widget)
        self.splitter.setSizes([250, 550]) # 초기 비율
        
        # 4. 하단 버튼 (확인, Revert)
        bottom_buttons_layout = QHBoxLayout()
        self.confirm_button = QPushButton('확인')
        self.revert_button = QPushButton('Revert')
        self.confirm_button.setObjectName("ConfirmButton")
        self.revert_button.setObjectName("RevertButton")
        
        bottom_buttons_layout.addStretch(1)
        bottom_buttons_layout.addWidget(self.confirm_button)
        bottom_buttons_layout.addWidget(self.revert_button)

        # 5. 메인 레이아웃에 조립
        self.main_layout.addWidget(self.splitter)
        self.main_layout.addLayout(bottom_buttons_layout)
        
        # 6. 초기 상태 및 예시 데이터
        self._setup_example_logs()
        self.log_details_tree.hide() # 상세 내용은 초기에 숨김
        
        # --- 시그널 연결 ---
        self.log_titles_tree.currentItemChanged.connect(self.on_log_title_selected)

    def _setup_example_logs(self):
        """ (임시) 예시 로그 데이터 채우기 """
        # TODO: 이 데이터는 나중에 DB나 파일에서 불러와야 함
        log1 = QTreeWidgetItem(self.log_titles_tree, ["컴퓨터강의자료 정리"])
        # (숨겨진 데이터)
        log1.setData(0, Qt.ItemDataRole.UserRole, [
            ["1", "00주차_강의자료.pdf", "Download -> C:\\...\\컴파일러개론"],
            ["2", "01주차_강의자료.pdf", "Download -> C:\\...\\컴파일러개론"]
        ])
        
        log2 = QTreeWidgetItem(self.log_titles_tree, ["251002_113002"])
        log2.setData(0, Qt.ItemDataRole.UserRole, [
            ["1", "증명서.hwp", "Download -> C:\\...\\문서\\증명서"]
        ])
        
        log3 = QTreeWidgetItem(self.log_titles_tree, ["01주차_강의자료.pdf"])
        log3.setData(0, Qt.ItemDataRole.UserRole, [
            ["1", "01주차_강의자료.pdf", "Download -> C:\\...\\임시"]
        ])
    
    @Slot(QTreeWidgetItem, QTreeWidgetItem)
    def on_log_title_selected(self, current_item, previous_item):
        """ 왼쪽 로그 제목 클릭 시 오른쪽 상세 내용 업데이트 """
        if current_item is None:
            self.log_details_label.show()
            self.log_details_tree.hide()
            return
            
        # 1. 숨겨둔 데이터 가져오기
        log_data = current_item.data(0, Qt.ItemDataRole.UserRole)
        
        # 2. 상세 트리 채우기
        self.log_details_tree.clear()
        if log_data:
            for item_data in log_data:
                tree_item = QTreeWidgetItem(self.log_details_tree, item_data)
                self.log_details_tree.addTopLevelItem(tree_item)
            
            self.log_details_tree.expandAll()
            
            # 3. 화면 전환
            self.log_details_label.hide()
            self.log_details_tree.show()
        else:
            # 데이터가 없는 경우
            self.log_details_label.setText("상세 내용이 없습니다.")
            self.log_details_label.show()
            self.log_details_tree.hide()