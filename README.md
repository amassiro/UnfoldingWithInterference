# UnfoldingWithInterference







# Install:

    cmssw-el7
    cmsrel CMSSW_11_3_4
    cd CMSSW_11_3_4/src

    cmsenv
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
    cd HiggsAnalysis/CombinedLimit
    git fetch origin
    git checkout v9.1.0
    
    cd ..
    git clone git@github.com:amassiro/UnfoldingWithInterference.git
    scramv1 b clean; scramv1 b -j 20 # always make a clean build

    

# Options

Definition of the different options available.

Definition of the signal samples (names in the datacard):


    --PO nameSignals=mysig
    
they can be more than one (separated by a comma):

    --PO nameSignals=mysig,mysecondsig

Definition of background samples that interfere with the signals (with all the signals):

    --PO nameBackgrounds=bkg

and also in this case the backgrounds can be more than one (separated by a comma).

Note that in the datacard there must be the "signal + background + interference" samples, for each signal:

    XX as signal
    sbi_XX is the signal + background + interference

If more than one background is defined previously, all of them must be added together in the sample "sbi_XX"


    
    
# How to run it:

    cd test 
    
    text2workspace.py      \
            test_datacard_1signal.txt   \
            -P HiggsAnalysis.UnfoldingWithInterference.UnfoldingWithInterference:unfoldingWithInterference  \
            -o   model_test.root    --X-allow-no-signal  \
            --PO nameSignals=mysig

or

    text2workspace.py      \
            test_datacard_1signal.txt   \
            -P HiggsAnalysis.UnfoldingWithInterference.UnfoldingWithInterference:unfoldingWithInterference  \
            -o   model_test.root    --X-allow-no-signal  \
            --PO nameSignals=mysig \
            --PO nameBackgrounds=bkg
            

    
    combine -M MultiDimFit model_test.root  --algo=grid --points 1000  -m 125   -t -1     \
        --redefineSignalPOIs CMS_mysig_mu \
        --setParameterRanges CMS_mysig_mu=0,10     \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"CMS_mysig_mu\"\)
    

    
    
    
    text2workspace.py      \
            test_datacard_2signals.txt   \
            -P HiggsAnalysis.UnfoldingWithInterference.UnfoldingWithInterference:unfoldingWithInterference  \
            -o   model_test.root    --X-allow-no-signal  \
            --PO nameSignals=mysig,mysecondsig
    
    
    combine -M MultiDimFit model_test.root  --algo=grid --points 1000  -m 125   -t -1     \
        --redefineSignalPOIs CMS_mysig_mu,CMS_mysecondsig_mu \
        --setParameterRanges CMS_mysig_mu=0,10:CMS_mysecondsig_mu=0,10    \
        --verbose -1
          
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"CMS_mysig_mu\"\)
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw.cxx\(\"CMS_mysecondsig_mu\"\)
    r99t higgsCombineTest.MultiDimFit.mH125.root  higgsCombineTest.MultiDimFit.mH125.root   draw2D.cxx\(\"CMS_mysig_mu\",\"CMS_mysecondsig_mu\",\"CMS_mysig_mu\",\"CMS_mysecondsig_mu\"\)

    
    
    
    
    
    
    