library(pcp)

try(pcp(iris))

try(pcp(1:5), silent=T)

try(pcp(list(x=1:10)), silent=T)

try(pcp(list(x=Inf, y=1:5)), silent=T)
