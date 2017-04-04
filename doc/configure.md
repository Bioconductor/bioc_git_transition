# Server

Git is hosted at the AWS-based server git.bioconductor.org

# svn 'authz' to gitolite 'conf'

The gitolite configuration involves

- ssh key files need to be named after svn user accounts (the end user
  does not need to know about this)

- uncomment `'continuation-lines'` to allow for `\` continuation lines
  (aesthetically useful for @bioconductor-write0, for instance).

- The following repositories have svn permissions but do not exist in
  Nitesh's clone, so gitolite created empty repositories:
  AffyTiling.git Agi4x44PreProcess.git BeadExplorer.git
  COPDSexualDimorphism.git ChromoViz.git DASiR.git DAVIDQuery.git
  DNaseR.git EpiCluster.git GA4GHclient.git GGexplorer.git
  GeneGroupAnalysis.git GeneR.git GeneRfold.git GeneSpring.git
  GeneTS.git GeneticsBase.git GenoView.git HTSeqGenieBase.git
  MMDiff.git RMAGEML.git RMAPPER.git RNASeqGenie.git RTools4TB.git
  RWebServices.git Rintact.git Rolexa.git STROMA4.git SemSim.git
  Seqnames.git SomatiCA.git SpliceGraph.git TimerQuant.git
  arrayMagic.git arrayQCplot.git asmn.git basePLM.git bim.git
  biocDatasets.git cellHTS.git cosmo.git cosmoGUI.git cydar.git
  exonmap.git fbat.git flowFlowJo.git flowPhyto.git flowTime.git
  gene2pathway.git gmapR2.git goCluster.git hdf5.git iFlow.git
  inSilicoDb.git inSilicoMerging.git jmosaics.git maDB.git
  makePlatformDesign.git maskBad.git metaX.git mmgmos.git mtbls2.git
  neaGUI.git netReg.git pairseqsim.git pgUtils.git prism.git spade.git
  stam.git virtualArray.git wiggleplotr.git xcmsGUI.git xmapcore.git

