library(tidyverse)

get_bioc_manifest <-
    function(manifest)
{
    args <- c("archive",
              "--remote=git@git.bioconductor.org:admin/manifest", "HEAD",
              manifest,"|" , "tar", "-x")
    system2("git", args, wait=TRUE)
    f <- readLines(manifest)
    f <- sub(
        "Package: *", "",
        regmatches(f, regexpr("Package:.*", f))
    )
    tbl_df(f)
}

get_packages_conf <-
    function(path = "/Users/ni41435_ca/Documents/gitolite-admin/conf/packages.conf")
{
    software <- readLines(path)
    idx <- grep("repo packages/", software)
    packs <- gsub("repo packages/", "",software[idx])
    tbl_df(packs)
}


## Get manifests
software <- get_bioc_manifest("software.txt")
data_exp <- get_bioc_manifest("data-experiment.txt")
workflows <- get_bioc_manifest("workflows.txt")

## Add type of package
software$type <- ""
data_exp$type <- "-dataexp-workflow"
workflows$type <- "-dataexp-workflow"

## bind rows
manifest <- bind_rows(software, data_exp, workflows)

## get packages conf
packages_conf <- get_packages_conf()

## packages to add to packages.conf
to_add <- anti_join(manifest, packages_conf)

## Write packages to temp file called packages.conf
write_file <-
    function(tbl)
{
    package_template <- paste0(
        "",
        "\nrepo packages/%s",
        "\n    RW master = @none",
        "\n    RW RELEASE_3_7 = @none",
        "\n    option hook.pre-receive = pre-receive-hook%s"
    )
    template = sprintf(package_template,
                       tbl$value,
                       tbl$type)
    template = paste(template, collapse="\n")
    write(template, file = "packages.conf", append=TRUE)
}
