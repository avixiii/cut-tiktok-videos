from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget, QLabel, QLineEdit, QPushButton, QTableWidgetItem, \
    QVBoxLayout, QTableWidget
from app.utils import open_dialog, get_video_info, click


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cut Tiktok Videos")
        self.setGeometry(100, 100, 1980, 1080)  # Set window position and size

        # Define edit text
        self.edt_input_folder = None
        self.edt_output_folder = None

        self.center_on_screen()

        # Create the sections
        self.create_config_section()
        self.create_preview_section()
        self.create_video_list_section()

    def center_on_screen(self):
        # Get the screen's geometry
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate the center position
        x = (screen_geometry.width() - self.width()) / 2
        y = (screen_geometry.height() - self.height()) / 2

        # Set the window position to the center
        self.move(x, y)

    def open_dialog(self):
        folder_path = open_dialog()

        if folder_path:
            self.edt_input_folder.setText(folder_path)
            self.populate_video_list(folder_path)

    def open_dialog_output(self):
        folder_path = open_dialog()

        if folder_path:
            self.edt_output_folder.setText(folder_path)

    def create_config_section(self):
        config_section = QWidget(self)
        config_section.setGeometry(0, 0, 400, 400)
        palette = config_section.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 255))
        config_section.setPalette(palette)

        label = QLabel("Input Folder", self)
        label.setGeometry(20, 20, 81, 16)
        self.edt_input_folder = QLineEdit(self)
        self.edt_input_folder.setGeometry(110, 20, 281, 21)
        input_btn = QPushButton('Browse', self)
        input_btn.setGeometry(400, 21, 100, 21)
        input_btn.clicked.connect(self.open_dialog)

        lb_output_folder = QLabel("Output Folder", self)
        lb_output_folder.setGeometry(10, 50, 91, 16)
        self.edt_output_folder = QLineEdit(self)
        # self.edt_output_folder.setGeometry(110, 80, 81, 21)
        self.edt_output_folder.setGeometry(110, 50, 281, 21)
        output_btn = QPushButton('Browse', self)
        output_btn.setGeometry(400, 44, 100, 21)
        output_btn.clicked.connect(self.open_dialog_output)

        lb_thread = QLabel("Thread", self)
        lb_thread.setGeometry(40, 80, 51, 16)
        edt_thread = QLineEdit(self)
        edt_thread.setGeometry(110, 80, 81, 21)

        lb_speed = QLabel("Speed", self)
        lb_speed.setGeometry(260, 80, 51, 16)
        edt_speed = QLineEdit(self)
        edt_speed.setGeometry(310, 80, 81, 21)

        lb_random_from = QLabel("Random from", self)
        lb_random_from.setGeometry(10, 110, 91, 16)
        edt_random_from = QLineEdit(self)
        edt_random_from.setGeometry(110, 110, 81, 21)

        lb_random_to = QLabel("Random to", self)
        lb_random_to.setGeometry(230, 110, 71, 16)
        edt_random_to = QLineEdit(self)
        edt_random_to.setGeometry(310, 110, 81, 21)

        lb_text_color = QLabel("Text Color", self)
        lb_text_color.setGeometry(10, 140, 91, 16)
        edt_text_color = QLineEdit(self)
        edt_text_color.setGeometry(110, 140, 81, 21)

        lb_text_size = QLabel("Text size", self)
        lb_text_size.setGeometry(240, 140, 61, 16)
        edt_text_size = QLineEdit(self)
        edt_text_size.setGeometry(310, 140, 81, 21)

        lb_part_define = QLabel("Part define", self)
        lb_part_define.setGeometry(230, 170, 71, 16)

        lb_out_aspect_ratio = QLabel("Out Aspect Ratio", self)
        lb_out_aspect_ratio.setGeometry(10, 170, 111, 16)

    def create_preview_section(self):
        # Create a widget for the preview section
        preview_section = QWidget(self)
        preview_section.setGeometry(self.width() - 200, 0, 200, 400)
        palette = preview_section.palette()
        palette.setColor(QPalette.Window, QColor(255, 0, 0))
        preview_section.setPalette(palette)

    def create_video_list_section(self):
        video_list_section = QWidget(self)
        video_list_section.setGeometry(0, 500, 1980, QDesktopWidget().screenGeometry().height() - 500)

        layout = QVBoxLayout(video_list_section)

        # Create a table to display the list
        table = QTableWidget()
        table.setColumnCount(7)  # Number of columns
        table.setObjectName("video_list_table")

        # Set table headers
        headers = ["Video Title", "Length(s)", "Duration", "Width:Height", "Aspect Ratio", "Message", "Status"]
        table.setHorizontalHeaderLabels(headers)
        table.setColumnWidth(0, 700)
        table.setColumnWidth(1, 130)
        table.setColumnWidth(2, 130)
        table.setColumnWidth(3, 130)
        table.setColumnWidth(4, 130)
        table.setColumnWidth(5, 600)
        table.setColumnWidth(6, 130)

        layout.addWidget(table)

    def populate_video_list(self, folder_path):
        video_info = get_video_info(folder_path)
        for video in video_info:
            video.append("16:9")
            video.append("")
            video.append("Waiting")
        table = self.findChild(QTableWidget, "video_list_table")

        if table is not None:
            table.setRowCount(len(video_info))
            print(video_info)
            for row, info in enumerate(video_info):
                for col, data in enumerate(info):
                    item = QTableWidgetItem(str(data))
                    table.setItem(row, col, item)
                    print(item)
