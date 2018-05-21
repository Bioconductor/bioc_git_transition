library(httr)
library(tidyverse)

BIOC_CREDENTIALS_PASSWORD = readLines("~/gitCredentialsAuth.txt")

auth <- authenticate(
    "nitesh.turaga@gmail.com",
    BIOC_CREDENTIALS_PASSWORD
)

.BIOC_CREDENTIALS_URL <-
    "https://git.bioconductor.org/BiocCredentials/api/biocusers/"

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
software$type <- "-software"
data_exp$type <- "-dataexp-workflow"
workflows$type <- "-dataexp-workflow"

## bind rows
manifest <- bind_rows(software, data_exp, workflows)

## get packages conf
# packages_conf <- get_packages_conf(path="/tmp/packages.conf")
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
        "\n    RW master = %s",
        "\n    RW RELEASE_3_7 = %s",
        "\n    option hook.pre-receive = pre-receive-hook%s"
    )
    template = sprintf(package_template,
                       tbl$value,
                       tbl$creds,
                       tbl$creds,
                       tbl$type)
    template = paste(template, collapse="\n")
    write(template, file = "packages.conf", append=TRUE)
}


get_maintainers_email <-
    function(package)
{
    args <- c("archive",
              paste0("--remote=git@git.bioconductor.org:packages/", package),
              "HEAD",
              "DESCRIPTION","|" , "tar", "-x")
    system2("git", args, wait=TRUE)
    dcf <- read.dcf(file.path("DESCRIPTION"))
    if ("Maintainer" %in% colnames(dcf)) {
        m <- dcf[, "Maintainer"]
        ret <- regexec("<([^>]*)>", m)[[1]]
        ml <- attr(ret, "match.length")
        email <- substr(m, ret[2], ret[2] + ml[2] - 1)
    }
    else if ("Authors@R" %in% colnames(dcf)) {
        ar <- dcf[, "Authors@R"]
        env <- new.env(parent = emptyenv())
        env[["c"]] = c
        env[["person"]] <- utils::person
        pp <- parse(text = ar, keep.source = TRUE)
        tryCatch(people <- eval(pp, env), error = function(e) {
            return()
        })
        for (person in people) {
            if ("cre" %in% person$role) {
                email <- person$email
            }
        }
    }
    c(package, email)
}


get_bioc_credentials <-
    function(email_id, auth)
{
    query <- paste0(.BIOC_CREDENTIALS_URL, "query_by_email/%s/")
    queries <- sprintf(query, email_id)
    content(httr::GET(queries, auth))
}


get_all <- function(package) {
    message("package: ", package)
    res <- get_maintainers_email(package)
    credential <- get_bioc_credentials(res[2], auth=auth)
    c(package, credential)
}


get_all_safely <- safely(get_all)

result <- to_add$value %>% map(get_all_safely)

t_result <- transpose(result)[["result"]]

## make a tbl with pacakge, credential
creds = tibble(value=unlist(sapply(t_result, `[[`, c(1))),
               creds=unlist(sapply(t_result, `[[`, c(2))))

## left_join (result_tbl, to_add) using value
to_add <- left_join(to_add, creds, by = c("value"))
to_add$creds <- str_replace_na(to_add$creds, "maintainer")
to_add$creds <- str_replace(to_add$creds, "maintainer",  "@bioconductor_writers")
to_add$creds[to_add$creds == ""] <- "@bioconductor_writers"

write_file(to_add)

## Packages in the packages.conf, but not in manifest
setdiff( packages_conf$value, manifest$value)
