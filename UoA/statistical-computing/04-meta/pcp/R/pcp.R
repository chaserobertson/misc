# matrix-plots a list with each variable on the x-axis,
# recycled and normalised values on the y-axis, 
# and configurable lines connecting each observations' values 
# todo: add a legend if line styles are not default :)
pcp <-
function(data, col=2, lwd=1, lty=1, ...) {
    
    # data argument must be a list
    if (!is.list(data))
        stop("`list' must be a list of variables!")
    
    # argument must have enough points to plot a line
    if (length(data) < 2)
        stop("Need at least two variables")
    
    # numericise and normalise all variables
    data <- normN(data)
    
    # will need to compare length of each variable
    n <- lengths(data)
    
    # use maximum variable length as matrix size
    N <- max(n)
    
    # recycle all variables to the same length
    if (!all(n == N))
        data <- lapply(data,
                       function(x) rep(x, length.out=N))
    
    # matplot needs a matrix as input
    m <- matrix(unlist(data), N)
    
    # restore variable names for output object
    colnames(m) <- names(data)
    
    # connect each observation's normalised values with a line 
    matplot(t(m), type='l', col=col, lwd=lwd, lty=lty, xlab='', ylab='', xaxt='n', yaxt='n', ...)
    
    # show x-axis gridlines
    abline(v = seq_along(data), col="#c0c0c0")
    
    # show x-axis with variable names
    axis(1, seq_along(data), names(data))
    
    # return data in normalised matrix form, but do not print
    invisible(data)
}
