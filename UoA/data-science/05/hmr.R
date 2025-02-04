## shell - Hadoop streaming
mapred streaming -input /data/airline/csv -output t1 -mapper 'wc -l' -reducer "awk '{N += \$1} END {print N}'"

## R + hmapred

## test on small subset - read from hdfs as bytes

r = readBin(pipe("hadoop fs -cat /data/airline/csv/2008.csv | head","rb"),
            raw(), 10000)

## parse only some columns

library(iotools)
d=dstrsplit(r,
	    list(NA,NA,NA,NA,NA,NA,NA,NA,carrier="",fln=1,NA,NA,NA,NA,NA,NA,NA,NA,dist=1),
	    sep=",", strict=FALSE)

## Note: can use read.csv.raw() for quick auto-detection
d = read.csv.raw(r)

## can create a "template"
ct = d[1,]
## or use c(name="class") form
ct = sapply(d, class)
## and set any unwanted ones to NA

library(hmapred)

res <- hmr(hinput("/data/airline/csv", 
            function(r) d=dstrsplit(r,
              list(NA,NA,NA,NA,NA,NA,NA,NA,carrier="",fln=1,NA,NA,NA,NA,NA,NA,NA,NA,dist=1),
              sep=",", strict=FALSE)),
	map = function(d) {
    	    ## remove NA distances
	    d = d[!is.na(d$dist),]
	    ## aggregate by carrier + flight number
	    a = aggregate(d$dist, list(flight=paste0(d$carrier,d$fln)),
	                ## to compute mean, need sum(x) / n separately
			function(x) c(sum=sum(x), n=length(x)))
	    ## extract the resulting matrix with columns sum and n
	    m = a$x
	    ## set the row names to flight - those will be the keys
	    rownames(m) = a$flight
	    m
	},
	## tryCatch is optional for debugging to return errors in
	## the data instead of failing the job (so would not use in
	## final code)
	reduce = function(m) tryCatch({
	   ## default is string matrix, convert to numeric
           storage.mode(m) = "numeric"
	   ## split by key, for each compute column sums = sum and n
           t(sapply(split(m, rownames(m)), function(x) colSums(matrix(x,,2))))
	}, error=function(e) as.character(e)),
	reducers=2 ## for demonstration, 
	)

## read the result
f = open(res, "rb")
r = readAsRaw(f)
close(f)
## parse into a matrix - use nsep="\t" if both key and values were used
m = mstrsplit(r, type="numeric", nsep="\t")
## compute mean (sum / n)
dmean = m[,1] / m[,2]
head(dmean)
## (in)famous AA-1 flight (NYC-LA)
dmean["AA1"]
##     AA1 
##2430.355 
