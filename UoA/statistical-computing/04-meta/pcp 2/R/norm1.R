# normalise numeric, factor or string vectors to numeric between 0 and 1
norm1 <-
function(x) {
    # character vectors cannot be normalised as-is
    if (is.character(x)) x <- factor(x)
    
    # factor vectors cannot be normalised as-is
    if (is.factor(x)) x <- as.integer(x)
    
    # ensure finite numeric before attempting normalisation
    if (!is.numeric(x) || !all(is.finite(x)))
        stop("All variables must finite numerics, factors or strings")
    
    # translate x such that its minimum value is 0
    x <- x - min(x)
    
    # scale x such that its maximum value is 1
    if (any(x > 0)) x / diff(range(x)) else x
}
