## Task: compute distribution of distances
## (binning by integers using tabulate())

## add two vectors padding with 0 to length as necessary
add.expand <- function(x,y, d = length(x) - length(y))
   if(d > 0) x + c(y, numeric(d)) else c(x, numeric(-d)) + y

library(iotools)
## read bzip2 file
f = bzfile("/course/data/nyctaxi/csv/yellow_tripdata_2010-01.csv.bz2", "rb")
## create chunk reader
r = chunk.reader(f)
## set initial state
distances <- 0
while (length(chunk <- read.chunk(r))) { ## read chunk
   ## parse chunk (select 5th column "trip_distance")
   d <- dstrsplit(chunk, list(NA, NA, NA, NA, dist=1),
                  sep=",", strict=FALSE)
   ## compute: bin distances
   new.dist <- tabulate(d$dist)
   ## update state: add new values expanding with 0
   distances <- add.expand(distances, new.dist)
   str(distances)
}
