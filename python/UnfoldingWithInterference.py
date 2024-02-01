from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

#
# Freely inspired by https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part2/physicsmodels/#signal-background-interference
#
# Generic interference model with arbitrary number of signals and backgrounds
# Usage: unfolded differential distribution --> many "signals", each with their own "intreference"
#
#

class UnfoldingWithInterference(PhysicsModel):

    "Float independently cross sections and branching ratios"
    def __init__(self):
        PhysicsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = ""
        self.prefixSignals = "sig"

        self.nameSignals = [
             'blabla',
             'blublu'
             ]
        self.numSignals = 2
        
        self.nameBackgrounds = [
             'bkg'
             ]
        self.numBackgrounds = 1
        
        

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith("nameSignals="):
                self.nameSignals = po.replace("nameSignals=","").split(",")
                print (" nameSignals = ", self.nameSignals)
                self.numSignals = len(self.nameSignals)
            if po.startswith("nameBackgrounds="):
                self.nameSignals = po.replace("nameBackgrounds=","").split(",")
                print (" nameBackgrounds = ", self.nameBackgrounds)
                self.numBackgrounds = len(self.nameBackgrounds)

 
#
# standard, not touched (end)
#


#
# Define parameters of interest
#

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""
        
        # trilinear Higgs couplings modified 
        self.modelBuilder.doVar("r[1,-10,10]")
        self.poiNames = "r"


        for signal_strength in range(0, self.numSignals):
          self.modelBuilder.doVar("CMS_" + str(self.nameSignals[signal_strength]) + "_mu[1, 0 ,100]")
          self.poiNames += ",CMS_" + str(self.nameSignals[signal_strength]) + "_mu"

        
        for signal_strength in range(0, self.numSignals):
          self.modelBuilder.factory_("expr::sig_" + str(signal_strength) + "_func(\"@0-sqrt(@0)\", CMS_" + self.nameSignals[signal_strength] + "_mu)")
          self.modelBuilder.factory_("expr::sbi_" + str(signal_strength) + "_func(\"sqrt(@0)\",    CMS_" + self.nameSignals[signal_strength] + "_mu)")
          
        backgroun_function_definition = "expr::bkg_func(\"1"
        for signal_strength in range(0, self.numSignals):
          backgroun_function_definition += " -sqrt(@0) "
        backgroun_function_definition += "\""
        for signal_strength in range(0, self.numSignals):
          backgroun_function_definition += ", CMS_" + self.nameSignals[signal_strength] + "_mu "
        backgroun_function_definition += ")"

        self.modelBuilder.factory_(backgroun_function_definition)

            
        print (" parameters of interest = ", self.poiNames)
        self.modelBuilder.doSet("POI",self.poiNames)


#
# Define how the yields change
#


    def getYieldScale(self,bin,process):

        for signal_strength in range(0, self.numSignals):
          if  process == self.nameSignals[signal_strength]:             return "sig_" + str(signal_strength) + "_func"
          if  process == "sbi_"+ self.nameSignals[signal_strength] :    return "sbi_" + str(signal_strength) + "_func"
      
        for background in range(0, self.numBackgrounds):
          if  process == self.nameBackgrounds[background]:             return "bkg_func"
         
        return 1



#
#  Inputs:
# 
#     S
#     S+B+I
#     B
#

unfoldingWithInterference = UnfoldingWithInterference()


