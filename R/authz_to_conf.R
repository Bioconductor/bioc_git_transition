## 
## Transform svn 'bioconductor.authz' to gitolite 'packages.conf'
##
## In a directory containing both bioc_git_transition and
## gitolite-admin repos, and with bioconductor.authz in
## bioc_git_transition/extdata, run
##
##     R -f bioc_git_transition/R/authz_to_conf.R

fin <- "bioc_git_transition/extdata/bioconductor.authz"
fout <- "gitolite-admin/conf/packages.conf"

remap_re <- "[']"                       # re-map userid characters to '_'
group_re <- "^[-[:alnum:]]+ *= (.*)"
repos_re <- "^\\[/trunk/madman/Rpacks/([[:alnum:]]+)]"

package_template <- paste(
    "repo packages/%s",
    "    RW master = %s",
    "    RW RELEASE_3_4 = %s",
    "",
    sep="\n"
)

stopifnot(file.exists(fin), !file.exists(fout))

group_formatter <- function(group_members, name) {
    txt <- sprintf(
        "%-79s\\",
        strwrap(
            group_members[name],
            initial = paste0("@", name, " = "),
            prefix = "    ", width = 70
        )
    )
    txt[length(txt)] <- sub(" *\\\\", "", txt[length(txt)])
    txt
}

pkgs <- system2(
    "svn",
    "list https://hedgehog.fhcrc.org/bioconductor/trunk/madman/Rpacks",
    stdout=TRUE
)
pkgs <- sub("/", "", pkgs[endsWith(pkgs, "/")])

authz <- trimws(readLines(fin))

grps <- grep(group_re, authz)
authz[grps] <- gsub(remap_re, "_", authz[grps])
authz[grps] <- gsub(", *", " ", authz[grps])
kv <- strsplit(authz[grps], " *= *")
group_members <- setNames(
    vapply(kv, `[[`, character(1), 2L),
    vapply(kv, `[[`, character(1), 1L)
)

repos <- grep(repos_re, authz)
name <- sub(repos_re, "\\1", authz[repos])
group <- sub(
    "@", "",
    vapply(strsplit(authz[repos + 1L], " *= *"), `[[`, character(1), 1L)
)
stopifnot(all(group %in% names(group_members)))
name <- name[group %in% pkgs]
group <- group[group %in% pkgs]

writers <- group_formatter(group_members, "bioconductor-write0")

fout <- file(fout, "w")
writeLines(c(
    writers,
    "",
    "repo @packages",
    "    R  = @all",
    "    RW master = @bioconductor-write0",
    "    RW RELEASE_3_4 = @bioconductor-write0",
    ""
), fout)

writeLines(
    sprintf(
        package_template,
        name,
        group_members[group],
        group_members[group]
    ),
    fout
)
close(fout)
