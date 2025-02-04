normN <-
function(data) 
    # convert to numeric and [0,1] normalise each of the argument list's contents
    lapply(data, norm1)
