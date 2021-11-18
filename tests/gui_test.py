import unittest

class GUITestCase(unittest.TestCase):
    def setUp(self):
        #self.NL = PairAnalysisCalculator()
        pass

    def test_Cp_Al_fcc(self):
        from debyetools.tpropsgui.gui import gui

        gui()

if __name__=='__main__':
    unittest.main()
