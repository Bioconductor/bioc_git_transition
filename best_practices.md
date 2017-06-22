# Bioconductor SVN to GIT transition

This package provides functionality to allow for SVN - Git transition for
the Bioconductor Project.

Goals:
* Create a private git server with all Bioconductor packages, including commit
  history from each of the _RELEASE_ branches and also the _devel_ branch.

Usage:
* This is a smaller test set of packages so your choices
are limited to a `List of available packages` (refer below).

* Clone a package:

  `git clone git@git.bioconductor.org:/packages/<package_of_choice>.git`

* See the branches available:

  ` cd ABarray`

  ` git branch -a`

* Checkout branch and see if the commit history is correct (most important step):

  `git checkout RELEASE_2_14`

  `git log`

* Make some changes from a copy and see if you can push back up, this should only be available if you have the private key. Not for a standard author.


### List of available packages: (A - D)
```
ABAEnrichment/
ABarray/
ABSSeq/
ACME/
ADaCGH2/
AffyCompatible/
AffyExpress/
AffyRNADegradation/
AGDEX/
AgiMicroRna/
AIMS/
ALDEx2/
AllelicImbalance/
AMOUNTAIN/
AnalysisPageServer/
Anaquin/
AneuFinder/
AnnotationDbi/
AnnotationForge/
AnnotationFuncs/
AnnotationHub/
AnnotationHubData/
AnnotationHubServer/
AnnotationHubServer.version0/
ArrayExpress/
ArrayExpressHTS/
ArrayTools/
ArrayTV/
ARRmNormalization/
ASAFE/
ASEB/
ASGSCA/
ASpli/
ASSET/
ASSIGN/
AtlasRDF/
BaalChIP/
BAC/
BADER/
BadRegionFinder/
BAGS/
BaseSpaceR/
Basic4Cseq/
BasicSTARRseq/
BatchQC/
BayesKnockdown/
BayesPeak/
BBCAnalyzer/
BCRANK/
BeadDataPackR/
BEAT/
BEclear/
BgeeDB/
BGmix/
BHC/
BicARE/
BiGGR/
Biobase/
BiocCaseStudies/
BiocCheck/
BiocCloud/
BiocContributions/
BiocFileCache/
BiocGenerics/
BiocInstaller/
BiocParallel/
BiocStyle/
BiocWorkflowTools/
BioMVCClass/
BioNet/
BioQC/
BioSeqClass/
Biostrings/
BiRewire/
BiSeq/
BitSeq/
BPRMeth/
BRAIN/
BrainStars/
BridgeDbR/
BrowserViz/
BrowserVizDemo/
BSgenome/
BubbleTree/
BufferedMatrix/
BufferedMatrixMethods/
BUMHMM/
BUS/
CAFE/
CAGEr/
CALIB/
CAMERA/
CancerInSilico/
CancerMutationAnalysis/
CancerSubtypes/
CAnD/
Cardinal/
Category/
CausalR/
CCPROMISE/
CellMapper/
CellNOptR/
CexoR/
CFAssay/
CGEN/
CGHbase/
CGHcall/
CGHnormaliter/
CGHregions/
ChAMP/
ChemmineOB/
ChemmineR/
Chicago/
ChIPComp/
ChIPexoQual/
ChIPpeakAnno/
ChIPQC/
ChIPseeker/
ChIPseqR/
ChIPsim/
ChIPXpress/
ChromHeatMap/
CHRONOS/
CINdex/
ClassifyR/
Clomial/
Clonality/
ClusterSignificance/
CMA/
CNAnorm/
CNEr/
CNExperiment/
CNORdt/
CNORfeeder/
CNORfuzzy/
CNORode/
CNPBayes/
CNTools/
CNVPanelizer/
CNVrd2/
CNVtools/
CoCiteStats/
CODEX/
CoGAPS/
COHCAP/
COMPASS/
CompGO/
ComplexHeatmap/
CONFESS/
ConsensusClusterPlus/
CopyNumber450k/
CopywriteR/
CoRegNet/
Cormotif/
CorMut/
CORREP/
COSNet/
CountClust/
CoverageView/
CRImage/
CRISPRseek/
CrispRVariants/
CSAR/
CSSP/
CVE/
CytoML/
DAPAR/
DART/
DBChIP/
DChIPRep/
DECIPHER/
DEDS/
DEFormats/
DEGraph/
DEGreport/
DEGseq/
```
