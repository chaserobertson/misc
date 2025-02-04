## Start R with sparkR in the hell

## read data (note: can also be a directory)
d=read.df("/data/nyctaxi/yellow/2009/yellow_tripdata_2009-01.parquet")

## the result is a data refrence, not teh actual contents:
d

## to read CSV files use, e.g.: read.df("...", "csv", header=TRUE)

## basic commands work
head(d)

## but others are just directives for furhter processing, not values
mean(d$Passenger_Count)

## they have to be applied to the data to work:
select(d, mean(d$Passenger_Count))

## the result is a descrition of the operation - to execute it,
## it must be "collected"
collect(select(d, mean(d$Passenger_Count)))

## subsetting just works and return another spark df reference
s = subset(d, d$Passenger_Count > 4)
s

head(s)

## but not all things work as expected
table(d$vendor_name)

## they have to be re-formulated based on supported opereations
## such as agg/sumarize and group_by
summarize(group_by(d, "vendor_name"), count = n(d$vendor_name))
collect(summarize(group_by(d, "vendor_name"), count = n(d$vendor_name)))

## rbind works - e.g. add another month of data:
d2=read.df("/data/nyctaxi/yellow/2009/yellow_tripdata_2009-02.parquet")
e=rbind(d, d2)

collect(summarize(group_by(e, "vendor_name"), count = n(e$vendor_name)))

## add all months of 2009 [Note that we could have simply used
## read.df("/data/nyctaxi/yellow/2009") in the beginning instead]
l = lapply(sprintf("/data/nyctaxi/yellow/2009/yellow_tripdata_2009-%02d.parquet", 3:12), read.df)
e = do.call(rbind, c(list(d, d2), l))

## our good friend payment type
collect(summarize(group_by(e, "payment_type"), count = n(e$payment_type)))

## re-code - but Spark uses upper() instead of toupper()
e$payment_type = upper(e$payment_type)

## check the distributions after recoding
collect(summarize(group_by(e, "payment_type"), count = n(e$payment_type)))

## how do the equivalent of table(d$payment_type, d$tip_amt > 0)?
collect(summarize(group_by(e, "payment_type"), tip = sum(e$Tip_Amt > 0)))

## does not work - "function sum requires numeric or interval types, not boolean"
## Spark does not coerce automaticaly, we have to "cast" varaibles to desired types
collect(summarize(group_by(e, "payment_type"), tip = sum(cast(e$Tip_Amt > 0, "bigint"))))

## to get both sides
collect(summarize(group_by(e, "vendor_name", "payment_type"),
                  tip = sum(cast(e$Tip_Amt > 0, "bigint")),
                  notip = sum(cast(e$Tip_Amt == 0, "bigint"))))
