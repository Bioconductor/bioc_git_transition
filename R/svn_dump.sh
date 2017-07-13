svnadmin create hedgehog.fhcrc.org
svnrdump dump https://hedgehog.fhcrc.org/bioconductor | svnadmin load hedgehog.fhcrc.org

svnadmin create bioc-data.hedgehog.fhcrc.org
svnrdump dump https://hedgehog.fhcrc.org/bioc-data | svnadmin load bioc-data.hedgehog.fhcrc.org

# Create svn dump and use this
mkdir hedgehog.fhcrc.org
cd hedgehog.fhcrc.org
svnadmin create bioconductor
svnrdump dump https://hedgehog.fhcrc.org/bioconductor | svnadmin load hedgehog.fhcrc.org/bioconductor
