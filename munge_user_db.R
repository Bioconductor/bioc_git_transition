txt = read.csv("users.txt",sep=" ",stringsAsFactors = FALSE,strip.white = T,header = FALSE)
csv = read.csv("user_db.csv",stringsAsFactors = FALSE)

present = txt$V1 %in% csv$SVN.User.ID

absent = txt[!present,]

head(csv)
csv[, "SVN.User.ID"] = ifelse(nzchar(csv$SVN.User.ID), csv$SVN.User.ID, csv$E.mail.Address)
csv[, "First.Name"] = ifelse(nzchar(csv$First.Name), csv$First.Name, csv$E.mail.Address)
csv[, "Last.Name"] = ifelse(nzchar(csv$Last.Name), csv$Last.Name, csv$E.mail.Address)


csv$svn = paste0(csv$SVN.User.ID," = ",csv$First.Name, " ", csv$Last.Name, " <",csv$E.mail.Address,">")
head(absent)
head(csv$svn)

dat = csv$svn
dat = rbind(dat,"(no author) = no_author <no_author@no_author>", "(no author) = no author no_author <noauthor@nowhere.com>")

head(absent)
View(absent)
result = c(dat, paste0(absent$V1, " = ", absent$V1, " ", absent$V1, " <", absent$V1, ">"))

# Munge
result[grep(pattern = "no",x = result)]
result = result[-1543]

result = data.frame(result)

result = rbind(result, 

write.table(result, file="user_db.txt",col.names=FALSE, row.names=FALSE, quote=FALSE)
