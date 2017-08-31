## 
## Transform svn 'bioconductor.authz' to gitolite 'packages.conf'
##
## In a directory containing both bioc_git_transition and
## gitolite-admin repos, and with bioconductor.authz in
## bioc_git_transition/extdata, run
##
##     R -f bioc_git_transition/R/authz_to_conf.R

fin <- "bioc_git_transition/extdata/bioconductor.authz"
fin2 <- "bioc_git_transition/extdata/bioc-data.authz"
fout <- "gitolite-admin/conf/packages.conf"
stopifnot(file.exists(fin), file.exists(fin2), !file.exists(fout))

remap_re <- "[']"                       # re-map userid characters to '_'
group_re <- "^[-.[:alnum:]]+ *= (.*)"

software_template <- paste(
    "repo packages/%s",
    "    RW master = %s",
    "    RW RELEASE_3_5 = %s",
    "    option hook.pre-receive = pre-receive-hook",
    "",
    sep="\n"
)

data_template <- paste(
    "repo packages/%s",
    "    RW master = %s",
    "    RW RELEASE_3_5 = %s",
    "",
    sep="\n"
)

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

process_authz <-
    function(fin, repos_re, reader_id, writer_id, svn_path = NA_character_)
{
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

    if (!is.na(svn_path)) {
        pkgs <- system2(
            "svn",
            paste0("list https://hedgehog.fhcrc.org", svn_path),
            stdout=TRUE
        )
        pkgs <- sub("/", "", pkgs[endsWith(pkgs, "/")])
    } else {
        pkgs <- group[!group %in% c(reader_id, writer_id)]
    }
    stopifnot(all(group %in% names(group_members)))
    group <- group[group %in% pkgs]

    list(
        writers = unname(group_members[writer_id]),
        group_members = group_members[group]
    )
}

group_merge <-
    function(..., id)
{
    writers <- unlist(strsplit(c(...), " "))
    writers <- paste0(sort(unique(writers)), collapse = " ")
    group_formatter(setNames(writers, id), id)
}

## bioconductor.authz

repos_re <- "^\\[/trunk/madman/Rpacks/([.[:alnum:]]+)]"
reader_id <- "bioconductor-readers"
writer_id <- "bioconductor-write0"
svn_path <- "/bioconductor/trunk/madman/Rpacks"
bioconductor_authz <-
    process_authz(fin, repos_re, reader_id, writer_id, svn_path)

repos_re <- "^\\[/trunk/experiment/pkgs/([.[:alnum:]]+)]"
reader_id <- "bioc-data_readers"
writer_id <- "bioc-data-writers"
svn_path <- "/bioc-data/trunk/experiment/pkgs"
bioc_data_authz <-
    process_authz(fin2, repos_re, reader_id, writer_id, svn_path)

writers <- group_merge(
    bioconductor_authz$writers,
    bioc_data_authz$writers,
    id = "bioconductor_writers"
)

fout <- file(fout, "w")
writeLines(c(
    writers,
    "",
    "repo @packages",
    "    R  = @all",
    "    RW master = @bioconductor-writers",
    "    RW RELEASE_3_5 = @bioconductor-writers",
    ""
), fout)

with(bioc_data_authz, {
    writeLines(
        sprintf(
            data_template,
            names(group_members),
            group_members,
            group_members
        ),
        fout
    )
})

with(bioconductor_authz, {
    writeLines(
        sprintf(
            software_template,
            names(group_members),
            group_members,
            group_members
        ),
        fout
    )
})

close(fout)
