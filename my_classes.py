from PyQt6 import QtWidgets, QtCore


# Class that allows operations to be performed by converting the type of data held in TableWidget cells to integer,
# which is its original type in string.
class NumericItem(QtWidgets.QTableWidgetItem):
    def __lt__(self, other):
        return (self.data(QtCore.Qt.ItemDataRole.UserRole) <
                other.data(QtCore.Qt.ItemDataRole.UserRole))