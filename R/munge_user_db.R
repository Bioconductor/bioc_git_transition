## svn log -q $svn | awk -F '|' '/^r/ {sub("^ ", "", $2); sub(" $", "", $2); print $2" = "$2" <"$2">"}' | sort -u > users.txt

fin1 <- "bioc_git_transition/extdata/users.txt"
fin2 <- "bioc_git_transition/extdata/user_db.csv"
fout <- "bioc_git_transition/extdata/user_db.txt"

txt <- readLines(fin1)
txt <- sub(
    "Jim Hester = Jim Hester <Jim Hester>",
    "Jim Hester = James Hester <jhester@fredhutch.org>",
    txt
)
txt <- cbind(strcapture(
    "(\\(?[[:alnum:].@ ]+\\)?) = .*", txt,
    data.frame(id=character(), stringsAsFactors=FALSE)
), data.frame(name="unknown", email="unknown", stringsAsFactors=FALSE))
idx <- grep("@", txt$id)
txt$email[idx] <- txt$id[idx]

csv <- read.csv(fin2, stringsAsFactors = FALSE)
csv[] <- lapply(csv, trimws)
csv$First.Name[csv$First.Name == "Martin Morgan"] <- "Martin"

csv$E.mail.Address[!nzchar(csv$E.mail.Address)] <- "unknown"

idx <- !nzchar(csv$SVN.User.ID) | csv$SVN.User.ID == "unknown"
csv$SVN.User.ID[idx] <- csv$E.mail.Address[idx]
csv$Name <- trimws(paste(csv$First.Name, csv$Last.Name))
csv$Name[!nzchar(csv$Name)] <- "unknown"

absent <- txt[!txt$id %in% csv$SVN.User.ID,]

fmt <- "%s = %s <%s>"
dat <- unique(c(
    sprintf(fmt, csv$SVN.User.ID, csv$Name, csv$E.mail.Address),
    sprintf(fmt, absent$id, absent$name, absent$email)
))

write.table(
    data.frame(dat), file=fout,
    col.names=FALSE, row.names=FALSE, quote=FALSE
)
