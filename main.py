from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSizePolicy
import sys
from PyQt6.QtCore import Qt

from cluster import VM, Rack, Server, Cluster

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CVMPS")
        self.setStyleSheet("background-color: lightblue;")
        self.resize(800,800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_style = """
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border: 2px solid #ffffff;
            }
        """
        start_btn = QPushButton (f"Start Builder")
        start_btn.setMinimumSize(150,40)
        start_btn.setMaximumSize(300,60)
        start_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        start_btn.setStyleSheet(button_style)
        start_btn.clicked.connect(self.button_clicked)
        layout.addWidget(start_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        continue_btn = QPushButton (f"Continue Build")
        continue_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        continue_btn.setStyleSheet(button_style)
        continue_btn.clicked.connect(self.button_clicked)
        continue_btn.setMinimumSize(150,40)
        continue_btn.setMaximumSize(300,60)
        layout.addWidget(continue_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        load_btn = QPushButton (f"Load Build")
        load_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        load_btn.setStyleSheet(button_style)
        load_btn.clicked.connect(self.button_clicked)
        load_btn.setMinimumSize(150,40)
        load_btn.setMaximumSize(300,60)
        layout.addWidget(load_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        options_btn = QPushButton (f"Options")
        options_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        options_btn.setStyleSheet(button_style)
        options_btn.clicked.connect(self.button_clicked)
        options_btn.setMinimumSize(150,40)
        options_btn.setMaximumSize(300,60)
        layout.addWidget(options_btn,alignment=Qt.AlignmentFlag.AlignCenter)

        quit_btn = QPushButton (f"Quit")
        quit_btn.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
        )
        quit_btn.setStyleSheet(button_style)
        quit_btn.clicked.connect(self.button_clicked)
        quit_btn.setMinimumSize(150,40)
        quit_btn.setMaximumSize(300,60)
        layout.addWidget(quit_btn,alignment=Qt.AlignmentFlag.AlignCenter)
    def button_clicked(self):
        print("You clicked!")

def clear_screen():
    # Optional: Clears terminal for a cleaner feel
    print("\033[H\033[J", end="")

# --- SCREEN FUNCTIONS ---



#def get_input_with_default(prompt, default_value):
#    """Returns user input or a default value if input is empty."""
#    user_input = input(f"{prompt} [Default Value: {default_value}]: ").strip()
#    return user_input if user_input else default_value


def add_rack_menu():
    print("=== NEW RACK ===")
    name = input("What would you like to name the Server Rack? ")
    slot_capacity = input("What is the rack unit height (U)? ")
    wattage = input("What is the wattage (W)? ")
    
#def add_server_menu():
#    print("=== NEW SERVER ===")
#    name = get_input_with_default("What is the server's name?", "Server's ID")
#    model = get_input_with_default("What is the server's model?", "Unknown")
#    size = get_input_with_default("What is the server's size (U)?", 1)
#    num_cpu = get_input_with_default("What is the number of CPUs that the server can hold?", "1")
#    new_server = Server(name, model, size, num_cpu)
#    print(repr(new_server))
#    input("\nPress Enter to return to confirm...")
#    return "NEW_BUILD"



# --- THE CONTROLLER ---

def run_app():
    # Initial State
    current_state = "MAIN"
    
    # Map states to their corresponding functions
    screens = {
        "MAIN": main_menu,
        "NEW_BUILD": new_build_menu,
        "LOAD_BUILD": load_build_menu,
        "ADD_SERVER": add_server_menu
    }

    while True:
        clear_screen()
        
        if current_state == "EXIT":
            print("Goodbye!")
            break
            
        # Execute the function for the current state
        # Each function returns the name of the NEXT state
        menu_function = screens.get(current_state)
        
        if menu_function:
            current_state = menu_function()
        else:
            print(f"Error: State {current_state} not found.")
            current_state = "MAIN"


def main():
   # app = QApplication(sys.argv)
   # window = MainWindow()
   # window.show()
   # sys.exit(app.exec())
  # test_1 = VM(1,"wowo","critical",0.8,0.7,0.9,10,100000,0.8)
  # print(test_1)
  # test_2 = VM(2,"wowo","utility",0.8,0.7,0.9,10,100000,0.8)
  # print(test_2)
  cluster = Cluster()
  cluster.main_menu()


if __name__ == "__main__":
    main()
