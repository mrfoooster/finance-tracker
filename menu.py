import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from financial_tracker import FinancialTracker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Financial Tracking App")
        self.setGeometry(200, 200, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.filename = ""
        self.tracker = FinancialTracker(filename=self.filename)

        self.create_account()

    def create_account(self):
        self.layout.addWidget(QLabel("Create a New Account"))

        self.currency_label = QLabel("Base Currency:")
        self.currency_input = QLineEdit()
        self.currency_input.setPlaceholderText("Enter base currency")
        self.layout.addWidget(self.currency_label)
        self.layout.addWidget(self.currency_input)

        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.clicked.connect(self.create_account_action)
        self.layout.addWidget(self.create_account_button)

        self.layout.addStretch()

    def create_account_action(self):
        base_currency = self.currency_input.text()
        self.tracker = FinancialTracker(base_currency=base_currency)

        self.layout.removeWidget(self.currency_label)
        self.layout.removeWidget(self.currency_input)
        self.layout.removeWidget(self.create_account_button)

        self.show_menu()

    def show_menu(self):
        self.layout.addWidget(QLabel("Menu"))

        self.import_button = QPushButton("Import Account")
        self.import_button.clicked.connect(self.import_account_action)
        self.layout.addWidget(self.import_button)

        self.add_transaction_button = QPushButton("Add Transaction")
        self.add_transaction_button.clicked.connect(self.add_transaction_action)
        self.layout.addWidget(self.add_transaction_button)

        self.plot_incomes_button = QPushButton("Plot Incomes")
        self.plot_incomes_button.clicked.connect(self.plot_incomes_action)
        self.layout.addWidget(self.plot_incomes_button)

        self.plot_outcomes_button = QPushButton("Plot Outcomes")
        self.plot_outcomes_button.clicked.connect(self.plot_outcomes_action)
        self.layout.addWidget(self.plot_outcomes_button)

        self.plot_balance_button = QPushButton("Plot Balance")
        self.plot_balance_button.clicked.connect(self.plot_balance_action)
        self.layout.addWidget(self.plot_balance_button)

    def import_account_action(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV files (*.csv)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.filename = selected_files[0]
            self.tracker = FinancialTracker(filename=self.filename)

    def add_transaction_action(self):
        # Implement your logic to add a transaction here
        pass

    def plot_incomes_action(self):
        self.plot_graph(self.tracker.plot_incomes)

    def plot_outcomes_action(self):
        self.plot_graph(self.tracker.plot_outcomes)

    def plot_balance_action(self):
        self.plot_graph(self.tracker.plot_balance)

    def plot_graph(self, plot_function):
        currency = self.tracker.base_currency
        plot_function(currency)

        # Create a separate window for the plotted graph
        graph_window = QMainWindow()
        graph_widget = QWidget()
        graph_layout = QVBoxLayout(graph_widget)
        graph_window.setCentralWidget(graph_widget)

        # Add the plotted graph to the layout
        graph_label = QLabel()
        graph_label.setAlignment(Qt.AlignCenter)
        graph_label.setPixmap(QPixmap("graph.png"))  # Assuming the graph is saved as "graph.png"
        graph_layout.addWidget(graph_label)

        graph_window.setWindowTitle("Plotted Graph")
        graph_window.setGeometry(300, 300, 600, 400)
        graph_window.show()

    def closeEvent(self, event):
        self.tracker.write_csv_file()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
