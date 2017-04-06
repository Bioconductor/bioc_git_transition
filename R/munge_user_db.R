## svn log -q $svn | awk -F '|' '/^r/ {sub("^ ", "", $2); sub(" $", "", $2); print $2" = "$2" <"$2">"}' | sort -u > users.txt

fin1 <- "bioc_git_transition/extdata/users.txt"
fin2 <- "bioc_git_transition/extdata/user_db.csv"
fout <- "bioc_git_transition/extdata/user_db.txt"

txt = read.csv(
    fin1,sep=" ",stringsAsFactors = FALSE,strip.white = T,header = FALSE
)
csv = read.csv(fin2,stringsAsFactors = FALSE)

present = txt$V1 %in% csv$SVN.User.ID

absent = txt[!present,]

head(csv)
csv[, "SVN.User.ID"] = ifelse(
    nzchar(csv$SVN.User.ID), csv$SVN.User.ID, csv$E.mail.Address
)
csv[, "First.Name"] = ifelse(
    nzchar(csv$First.Name), csv$First.Name, csv$E.mail.Address
)
csv[, "Last.Name"] = ifelse(
    nzchar(csv$Last.Name), csv$Last.Name, csv$E.mail.Address
)


csv$svn = paste0(
    csv$SVN.User.ID," = ",csv$First.Name, " ", csv$Last.Name, " <",
    csv$E.mail.Address,">"
)
head(absent)
head(csv$svn)

dat = csv$svn
dat = rbind(
    dat,"(no author) = no_author <no_author@no_author>",
    "(no author) = no author no_author <noauthor@nowhere.com>"
)

head(absent)
View(absent)
result = c(
    dat,
    paste0(absent$V1, " = ", absent$V1, " ", absent$V1, " <", absent$V1, ">")
)

# Munge
result[grep(pattern = "no",x = result)]
result = result[-1543]

result = data.frame(result)

write.table(
    result, file=fout,col.names=FALSE, row.names=FALSE, quote=FALSE
)
