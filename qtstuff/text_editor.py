import sys
import re
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTextEdit, QMessageBox, QLabel, QGridLayout, QTabWidget, QFileDialog
from PyQt6.QtGui import QAction, QKeySequence
import PyQt6.QtCore as Qtc

# constants for conversions
PREFIX = "!"
NORMAL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
SUPER_SCRIPT = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
SUB_SCRIPT = "ₐ₈CDₑբGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥwₓᵧZₐ♭꜀ᑯₑբ₉ₕᵢⱼₖₗₘₙₒₚ૧ᵣₛₜᵤᵥwₓᵧ₂₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"


# utility functions
def get_super(text: str):
    res = text.maketrans(''.join(NORMAL), ''.join(SUPER_SCRIPT))
    return text.translate(res)

def get_sub(text: str):
    res = text.maketrans(''.join(NORMAL), ''.join(SUB_SCRIPT))
    return text.translate(res)

def sqrt(text: str):
    """This is more of a placeholder function to work with the existing methods in MainWindow"""
    return text


RULES = { # first parameter is function which replaces trailing characters with something, 
# second parameter is string to replace said character 
    "_": [get_sub, ""],
    "^": [get_super, ""],
    PREFIX + "sqrt": [None, "√"],
    PREFIX + "alpha": [None, "α"],
    PREFIX + "beta": [None, "β"],
    PREFIX + "gamma": [None, "γ"],
    PREFIX + "delta": [None, "Δ"],
    PREFIX + "epsilon": [None, "ε"],
    PREFIX + "theta": [None, "θ"],
    PREFIX + "mu": [None, "μ"],
    PREFIX + "lambda": [None, "λ"],
    PREFIX + "pi": [None, "π"],
    PREFIX + "sigma": [None, "Σ"],
    PREFIX + "omega": [None, "Ω"],
    PREFIX + "deg": [None, "°"],
    PREFIX + "union": [None, "∪"],
    PREFIX + "intersect": [None, "∩"]
}


class CheatSheetWindow():
    def __init__(self) -> None:
        self.widget = QWidget()
        layout = QGridLayout()
        
        text = "Press Ctrl+Space to convert selected text \
        \nPress Ctrl+N to create a new tab \
        \nPress Ctrl+W to close the current tab\n\n"

        for key in RULES:
            if RULES[key][0] is None:
                text += f"{key} -> {RULES[key][1]} \n"

        label = QLabel(text)

        layout.addWidget(label, 0, 0, Qtc.Qt.AlignmentFlag.AlignCenter)
        self.widget.setLayout(layout)


class TextEditor(QTextEdit):
    def __init__(self) -> None:
        super().__init__()

        self._start_selection = 0
        self._end_selection = 0
        self.saved = True
        self._selected_text = ""

        self.textChanged.connect(self._not_saved)

    def _not_saved(self):
        self.saved = False
    
    def _convert_string_with_rule(self, string: str, character_key: str):
        index = string.find(character_key)
        if index == -1: return string
        
        # get current text that's on the editor   
        current_text = self.toPlainText()
        # removing the selected string from the text, so we only operate on a small snippet.

        index_of_selected_string = current_text.find(string, self._start_selection, self._end_selection)
        string_to_add_to = list(current_text.replace(string, "", 1))
        string = string.replace(character_key, RULES[character_key][1], 1)
        string_list = list(string)

        # iterate through the selected string
        if RULES[character_key][0] is not None:
            for i in range(index, len(string)):
                # get the character
                char = string_list[i]

                # check if the character is valid
                if NORMAL.find(char) == -1:
                    break
                replacement_char = RULES[character_key][0](char)
                string_list[i] = replacement_char
                        
        string = "".join(string_list)
        
        string_to_add_to.insert(index_of_selected_string, string)
        final_string = "".join(string_to_add_to)
        self.setPlainText(final_string)

        # recursion, keep going through until all instances are replaced. 
        return self._convert_string_with_rule(string, character_key)

    def modify_selected_text(self):
        """Wrapper function which sets the parameters needed for _convert_string_with_rule"""
        cursor = self.textCursor()
        current_text = self.toPlainText()
        if cursor.anchor() > cursor.position():
            self._end_selection = cursor.anchor()
            self._start_selection = cursor.position()
        else:
            self._end_selection = cursor.position()
            self._start_selection = cursor.anchor()
        self._selected_text = current_text[self._start_selection:self._end_selection]
        for _, v in enumerate(RULES):
            self._selected_text = self._convert_string_with_rule(self._selected_text, v)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text editor")

        self._path = ""

        # text editor window
        self.cheat_sheet = CheatSheetWindow()
        # tabs
        tabwidget = QTabWidget()
        tabwidget.addTab(self.cheat_sheet.widget, "Help")

        self.setCentralWidget(tabwidget)

        # text_editor_actions
        format_action = QAction("Format", self)
        format_action.setShortcut(QKeySequence("Ctrl+Space"))
        format_action.triggered.connect(self._format_current_text)
        tabwidget.addAction(format_action)

        # tab_actions
        new_tab = QAction("New tab", self)
        new_tab.setShortcut(QKeySequence("Ctrl+N"))
        new_tab.triggered.connect(self._new_tab)
        tabwidget.addAction(new_tab)

        close_tab = QAction("Close tab", self)
        close_tab.setShortcut(QKeySequence("Ctrl+W"))
        close_tab.triggered.connect(self._close_tab)
        tabwidget.addAction(close_tab)

        # menu_bar 
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self._file_save)
        file_menu.addAction(save_action)

        save_action = QAction("Save as", self)
        save_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_action.triggered.connect(self._file_save_as)
        file_menu.addAction(save_action)

    def _save_dialogue(self) -> bool:
        """Returns boolean value if user pressed yes/no"""
        message_box = QMessageBox(QMessageBox.Icon.Warning, "Wait a minute!", "You haven't saved this file. Do you want to save?")
        message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel)
        user_reply = message_box.exec()
        if user_reply == QMessageBox.StandardButton.Yes:
            self._file_save()
        elif user_reply == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def _format_current_text(self):
        current_widget: TextEditor = self.centralWidget().currentWidget()
        if current_widget == self.cheat_sheet.widget: return
        current_widget.modify_selected_text()
    
    def _new_tab(self):
        tab_widget: QTabWidget = self.centralWidget()
        tab_widget.setCurrentIndex(tab_widget.addTab(TextEditor(), "new file"))

    def _close_tab(self):
        tab_widget: QTabWidget = self.centralWidget()
        if tab_widget.currentWidget() == self.cheat_sheet.widget: return
        current_widget = tab_widget.currentWidget()
        if not current_widget.saved:
            if not self._save_dialogue():
                return
        tab_widget.removeTab(tab_widget.currentIndex())

    def _open_file(self):
        self._new_tab()
        tab_widget: QTabWidget = self.centralWidget()
        current_widget = tab_widget.currentWidget()
        name = QFileDialog.getOpenFileName(self, 'Open File')
        if name[0] == "": return
        self._path = name[0]
        with open(name[0], "r") as f:
            text = f.read()
            current_widget.setPlainText(text)
            tab_widget.setTabText(tab_widget.currentIndex(), f.name)

    def _file_save(self):
        current_widget = self.centralWidget().currentWidget()
        if current_widget == self.cheat_sheet.widget: return
        if self._path == "": 
            self._file_save_as()
            return
        with open(self._path, "w") as f:
            text = current_widget.toPlainText()
            f.write(text)

    def _file_save_as(self):
        tab_widget: QTabWidget = self.centralWidget()
        current_widget = tab_widget.currentWidget()
        if current_widget == self.cheat_sheet.widget: return

        name = QFileDialog.getSaveFileName(self, 'Save File')
        if name[0] == "": return
        self._path = name[0]
        with open(name[0], "w") as f:
            text = current_widget.toPlainText()
            f.write(text)
            tab_widget.setTabText(tab_widget.currentIndex(), f.name)
        

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
