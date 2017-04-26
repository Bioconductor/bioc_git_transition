svnadmin create hedgehog.fhcrc.org
svnrdump dump https://hedgehog.fhcrc.org/bioconductor | svnadmin load hedgehog.fhcrc.org

svnadmin create bioc-data.hedgehog.fhcrc.org
svnrdump dump https://hedgehog.fhcrc.org/bioc-data | svnadmin load bioc-data.hedgehog.fhcrc.org
