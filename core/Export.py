from matplotlib.backends.backend_pdf import PdfPages
from pylab import *

from core.Logging import myLogger


class Pdf(object):
    """ this class handles the export of the pyplane plots
    
    """

    def __init__(self, graph):
        self.myGraph = graph

        #        self.filename = 'pypypyplane_export.pdf'

        self.pdf = PdfPages('pyplane_export.pdf')

        # phaseplane -----------------------------------------
        ##
        #        QtCore.pyqtRemoveInputHook()
        #        embed()
        #        self.subplot_pp = pyplot.subplot2grid((3,1), (0,0), rowspan=1, colspan=1)
        #        self.subplot_pp.ax = self.myGraph.plot_pp.axes
        #        self.subplot_pp.fig = Figure(figsize=(400,400))
        #        self.subplot_x = pyplot.subplot2grid((3,1), (1,0), rowspan=1, colspan=1)
        #        self.subplot_x.ax = self.myGraph.plot_x.axes
        #        self.subplot_y = pyplot.subplot2grid((3,1), (2,0), rowspan=1, colspan=1)
        #        self.subplot_y.ax = self.myGraph.plot_y.axes

        #        pyplot.tight_layout()
        self.pdf.savefig(self.myGraph.plot_pp.fig)
        # x(t) -----------------------------------------------
        # self.pdf.savefig(self.myGraph.plot_x.fig)
        #        self.subplot_x = self.myGraph.plot_x

        # y(t) -----------------------------------------------
        # self.pdf.savefig(self.myGraph.plot_y.fig)
        #        self.subplot_y = self.myGraph.plot_y


        #        pyplot.show()
        self.pdf.close()
        myLogger.message = ("pdf export complete")

    def askForFilename(self):
        pass


    def setFilename(self, filename):
        self.filename = filename


    def createPdf(self):
        pass
