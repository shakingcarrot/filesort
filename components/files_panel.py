import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QTextEdit, QPushButton, QHeaderView, QCheckBox
)
from PySide6.QtCore import Qt, Slot, Signal
from components.directory_bar import DirectoryBar 

class FilesPanel(QWidget):
    """ 'files' 탭 (DirectoryBar 포함) """
    
    def __init__(self):
        super().__init__()
        self.setObjectName("FilesPanel") 
        self.current_path = ""
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.dir_bar = DirectoryBar()
        self.main_layout.addWidget(self.dir_bar)

        # 3. 'Ask' 상태 위젯
        self.ask_widget = QWidget()
        self.ask_widget.setObjectName("AskWidget") # (중요) ID 설정
        ask_layout = QVBoxLayout(self.ask_widget)
        ask_layout.setContentsMargins(15, 15, 15, 15)
        ask_layout.setSpacing(10)
        
        self.file_tree = QTreeWidget()
        self.file_tree.setObjectName("FileTree")
        self.file_tree.setHeaderLabels(['files'])
        self.file_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        self.ask_edit = QTextEdit()
        self.ask_edit.setPlaceholderText('Ask anything...')
        self.ask_edit.setMaximumHeight(100)
        self.ask_edit.setObjectName("AskEdit")
        
        self.organize_button = QPushButton('정리')
        self.organize_button.setObjectName("OrganizeButton")
        
        ask_layout.addWidget(self.file_tree)
        ask_layout.addWidget(self.ask_edit)
        ask_layout.addWidget(self.organize_button)

        # 4. 'Preview' 상태 위젯
        self.preview_widget = QWidget()
        self.preview_widget.setObjectName("PreviewWidget") # (중요) ID 설정
        preview_layout = QVBoxLayout(self.preview_widget)
        preview_layout.setContentsMargins(15, 15, 15, 15)
        preview_layout.setSpacing(10)
        
        self.select_all_checkbox = QCheckBox("전체 선택 / 해제")
        self.select_all_checkbox.setObjectName("SelectAllCheckbox")
        
        self.preview_tree = QTreeWidget()
        self.preview_tree.setObjectName("PreviewTree")
        self.preview_tree.setHeaderLabels(['번호', '파일', '원래 경로', '이동될 위치'])
        self.preview_tree.header().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.preview_tree.header().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.preview_tree.header().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.preview_tree.header().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        preview_buttons_layout = QHBoxLayout()
        self.delete_button = QPushButton('삭제')
        self.move_button = QPushButton('이동')
        self.cancel_button = QPushButton('취소')
        self.delete_button.setObjectName("DeleteButton")
        self.move_button.setObjectName("MoveButton")
        self.cancel_button.setObjectName("CancelButton")
        
        preview_buttons_layout.addStretch(1)
        preview_buttons_layout.addWidget(self.delete_button)
        preview_buttons_layout.addWidget(self.move_button)
        preview_buttons_layout.addWidget(self.cancel_button)
        
        preview_layout.addWidget(self.select_all_checkbox)
        preview_layout.addWidget(self.preview_tree)
        preview_layout.addLayout(preview_buttons_layout)

        # 5. 메인 레이아웃에 두 위젯 추가 및 초기 상태 설정
        self.main_layout.addWidget(self.ask_widget)
        self.main_layout.addWidget(self.preview_widget)
        self.preview_widget.hide()
        
        # --- 시그널 연결 ---
        self.organize_button.clicked.connect(self.show_organize_preview)
        self.cancel_button.clicked.connect(self.show_ask_view)
        
        self.select_all_checkbox.toggled.connect(self.toggle_all_previews)
        self.preview_tree.itemChanged.connect(self.update_select_all_checkbox_state)
        
        self.dir_bar.directory_changed.connect(self.update_directory)
        
        self.update_directory(self.dir_bar.get_current_path())

    @Slot(str)
    def update_directory(self, new_path):
        self.current_path = new_path
        self.load_files_from_path(new_path)
        self.show_ask_view()

    def load_files_from_path(self, path_str):
        self.file_tree.clear()
        
        try:
            if not os.path.isdir(path_str):
                QTreeWidgetItem(self.file_tree, [f"오류: 경로를 찾을 수 없습니다."])
                return

            files = [f for f in os.listdir(path_str) if os.path.isfile(os.path.join(path_str, f))]
            
            parent_item = QTreeWidgetItem(self.file_tree, [f"{len(files)} Files"])
            parent_item.setFlags(parent_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            parent_item.setCheckState(0, Qt.CheckState.Unchecked)

            for file_name in files:
                child_item = QTreeWidgetItem(parent_item, [file_name])
                child_item.setFlags(child_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                child_item.setCheckState(0, Qt.CheckState.Checked)

            self.file_tree.expandAll()

        except Exception as e:
            self.file_tree.clear()
            QTreeWidgetItem(self.file_tree, [f"파일 로드 오류: {e}"])

    def show_organize_preview(self):
        checked_files_data = [] 
        prompt_text = self.ask_edit.toPlainText()

        root = self.file_tree.invisibleRootItem()
        parent_item = None
        if root.childCount() > 0 and "Files" in root.child(0).text(0):
             parent_item = root.child(0)

        if parent_item:
            for i in range(parent_item.childCount()):
                child = parent_item.child(i)
                if child.checkState(0) == Qt.CheckState.Checked:
                    full_path = os.path.join(self.current_path, child.text(0))
                    checked_files_data.append([child.text(0), full_path])
        
        self.preview_tree.clear()
        for i, (file_name, original_path) in enumerate(checked_files_data):
            if "사진" in prompt_text:
                new_destination = f"사진/{file_name}"
            elif "문서" in prompt_text:
                new_destination = f"문서/{file_name}"
            else:
                new_destination = f"정리된 파일/{file_name}"
            
            item = QTreeWidgetItem(self.preview_tree, [str(i+1), file_name, original_path, new_destination])
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(0, Qt.CheckState.Checked)
        
        self.preview_tree.expandAll()
        
        self.update_select_all_checkbox_state(None, 0)

        self.ask_widget.hide()
        self.preview_widget.show()

    def show_ask_view(self):
        self.preview_widget.hide()
        self.ask_widget.show()

    @Slot(bool)
    def toggle_all_previews(self, checked):
        try:
            self.preview_tree.itemChanged.disconnect(self.update_select_all_checkbox_state)
        except RuntimeError:
            pass 

        root = self.preview_tree.invisibleRootItem()
        state = Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        for i in range(root.childCount()):
            item = root.child(i)
            item.setCheckState(0, state)
        
        self.preview_tree.itemChanged.connect(self.update_select_all_checkbox_state)

    @Slot(QTreeWidgetItem, int)
    def update_select_all_checkbox_state(self, item, column):
        try:
            self.select_all_checkbox.toggled.disconnect(self.toggle_all_previews)
        except RuntimeError:
            pass 

        root = self.preview_tree.invisibleRootItem()
        count = root.childCount()
        if count == 0:
            self.select_all_checkbox.setChecked(False)
            self.select_all_checkbox.toggled.connect(self.toggle_all_previews)
            return

        all_checked = True
        for i in range(count):
            if root.child(i).checkState(0) != Qt.CheckState.Checked:
                all_checked = False
                break
        
        self.select_all_checkbox.setChecked(all_checked)
        
        self.select_all_checkbox.toggled.connect(self.toggle_all_previews)