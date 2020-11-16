from PyQt5 import QtWidgets, uic, QtCore, QtGui
#from PyQt5.QtWidgets import QLabel
import sys
import datetime
import time

class Chrono(QtWidgets.QMainWindow):
    def __init__(self):
        super(Chrono, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('UI/cronometro.ui', self) # Load the .ui file
        self.show() # Show the GUI
        self.startStop.clicked.connect(self.start_crono)
        self.lap.clicked.connect(self.record_lap)
    

        self.laps_image = QtGui.QIcon('img/laps.png')
        self.restart_image = QtGui.QIcon('img/restart.png')
        self.start_image = QtGui.QIcon('img/white.png')
        self.pause_image = QtGui.QIcon('img/pause.png')

        self.lap_num = 0
        self.previous_time = 0
        self.paused = False
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_watch)
        self.timer.setInterval(1)
        self.mscounter = 0
        self.isreset = True
        self.showLCD() 

    def record_lap(self):
        """
        Afegeix una nova lap al cronómetro
        """
        this_time = datetime.timedelta(milliseconds=self.mscounter)
        if (self.mscounter != 0):
            self.lap_num += 1
            text = "Lap "+str(self.lap_num)+": "
            if(self.lap_num ==  1):
                text += str(this_time)[2:-3]
            else:
                text += str(this_time - self.previous_time)[2:-3]
            
            self.previous_time = this_time
            label = QtWidgets.QLabel(text)
            label.setAlignment(QtCore.Qt.AlignCenter)
            self.lapsLayout.addWidget(label)


    def showLCD(self):
        """
        Aquesta funció serveix per a mostrar per pantalla el temps
        """
        text = str(datetime.timedelta(milliseconds=self.mscounter))[:-3]
        self.cronNum.setDigitCount(8)
        if not self.isreset:  # si "isreset" es False
            self.cronNum.display(text)
        else:
            self.cronNum.display('0:00.000')

    def run_watch(self):
        """
        Executa el cronómetre de forma interna
        """
        self.mscounter += 1
        self.showLCD()

    def start_crono(self):
        """
        Comença el cronómetre de forma visible
        """
        self.timer.start()
        

        self.lap.setIcon(self.laps_image)
        if(self.isreset == False):
            self.lap.clicked.disconnect(self.reset_watch)
            self.lap.clicked.connect(self.record_lap)

        self.startStop.setIcon(self.pause_image)
        self.startStop.clicked.disconnect(self.start_crono)
        self.startStop.clicked.connect(self.pause_watch)
        self.isreset = False
        
    def pause_watch(self):
        """
        Pausa el cronómetre
        """

        self.timer.stop()

        self.startStop.setIcon(self.start_image)
        self.startStop.clicked.disconnect(self.pause_watch)
        self.startStop.clicked.connect(self.start_crono)

        self.lap.setIcon(self.restart_image)
        self.lap.clicked.disconnect(self.record_lap)
        self.lap.clicked.connect(self.reset_watch)
    
    def reset_watch(self):
        """
        Reinicia el cronómetre
        """
        self.timer.stop()
        self.mscounter = 0
        self.lap_num = 0
        self.isreset = True
        self.previous_time = 0
        self.showLCD()

        self.startStop.setIcon(self.start_image)



        self.lap.setIcon(self.laps_image)
        self.lap.clicked.disconnect(self.reset_watch)
        self.lap.clicked.connect(self.record_lap)


        for i in reversed(range(self.lapsLayout.count())): # Esborra totes les laps
            self.lapsLayout.itemAt(i).widget().setParent(None)
        

# Eliminar aço despres de acabar les proves ja que no volem que es puga executar
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
    window = Chrono() # Create an instance of our class
    app.exec_() # Start the application