import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from main_window import MainAppWindow

# QTabWidget 레이아웃 스타일시트
TAB_LAYOUT_STYLESHEET = """
    /* -------------------
       1. 전체 앱 스타일
       ------------------- */
    * {
        font-family: 'Inter', -apple-system;
        font-size: 13px;
    }

    /* -------------------
       2. 상단 바 (검정색 배경)
       ------------------- */
    #DirectoryBar {
        background-color: #1E1E1E;
        min-height: 40px;
        padding: 0px;
        margin: 0px;
    }

    #DirectoryBar QLabel {
        color: white;
    }

    #DirectoryBar #DirectoryPathEdit {
        background-color: #1E1E1E;
        color: white;
        border: none;
        padding: 2px 4px;
    }

    #DirectoryBar #BrowseButton {
        color: white;
        background-color: transparent;
        border: none;
        width: 16px;
        height: 16px;
    }

    /* -------------------
       2. 탭 바 (검정색 배경)
       ------------------- */
    QTabWidget::pane {
        border: none;
        background-color: white;
        margin: 0px;
    }
    
    QTabBar {
        background-color: #1E1E1E;
    }
    
    QTabBar::tab {
        background-color: #1E1E1E;
        color: #CCCCCC;
        border: none;
        padding: 8px 20px;
        min-width: 80px;
        margin: 0px;
    }
    
    QTabBar::tab:selected {
        color: white;
        border-bottom: 1px solid #0078D4;
    }
    
    QTabBar::tab:hover {
        color: white;
    }

    /* -------------------
       3. 트리 위젯 스타일
       ------------------- */
    QTreeWidget {
        background-color: white;
        border: none;
        margin: 0px;
        padding: 5px;
    }
    
    QTreeWidget::item {
        height: 25px;
        color: black;
    }
    
    QTreeWidget::item:selected {
        background-color: #E5F3FF;
        color: black;
    }
    
    QHeaderView::section {
        background-color: white;
        border: none;
        border-bottom: 1px solid #E5E5E5;
        color: black;
        padding: 4px;
    }
    
    /* Checkbox 스타일 */
    QTreeWidget::indicator {
        width: 16px;
        height: 16px;
    }
    
    QTreeWidget::indicator:unchecked {
        border: 1px solid #CCCCCC;
        background: white;
        border-radius: 3px;
    }
    
    QTreeWidget::indicator:checked {
        background-color: #0078D4;
        border: none;
        border-radius: 3px;
    }

    /* -------------------
       4. 입력 필드 및 버튼
       ------------------- */
    QTextEdit {
        border: 1px solid #CCCCCC;
        border-radius: 4px;
        padding: 8px;
        color: #666666;
    }
    
    QPushButton {
        background-color: #0078D4;
        color: white;
        border: none;
        border-radius: 2px;
        padding: 5px 15px;
        min-width: 80px;
        height: 28px;
    }
    
    QPushButton:hover {
        background-color: #106EBE;
    }
    
    QPushButton:pressed {
        background-color: #005A9E;
    }
    
    /* Ask anything... placeholder */
    QTextEdit[placeholderText] {
        color: #666666;
    }


    /* -------------------
       5. LogPanel 내부
       ------------------- */
    #LogPanel {
        background-color: #FFFFFF;
    }
    #LogPanelSplitter::handle {
        background-color: #DCDCDC;
    }
    #LogPanelSplitter::handle:horizontal {
        width: 1px;
    }
    #LogPanel #ConfirmButton, #LogPanel #RevertButton {
        background-color: #0078D4;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        padding: 8px 15px;
        font-weight: bold;
    }
    #LogPanel #ConfirmButton:hover { background-color: #005A9E; }
    #LogPanel #RevertButton:hover { background-color: #005A9E; }
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    app.setStyle(QStyleFactory.create('Fusion'))
    
    app.setStyleSheet(TAB_LAYOUT_STYLESHEET)
    
    window = MainAppWindow()
    window.show()
    sys.exit(app.exec())