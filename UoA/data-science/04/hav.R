hav <- function(m, p, r=6378137) {
    m <- m / 180 * pi
    p <- p / 180 *pi
    dLat <- m[,1] - p[1]
    dLon <- m[,2] - p[2]
    a <- (sin(dLat/2))^2 + cos(p[1]) * cos(m[,1]) * (sin(dLon/2))^2
    a <- pmin(a, 1)
    2 * atan2(sqrt(a), sqrt(1 - a)) * r
}

havr <- function(m, p, r=6378137) {
    dLat <- m[,1] - p[1]
    dLon <- m[,2] - p[2]
    a <- (sin(dLat/2))^2 + cos(p[1]) * cos(m[,1]) * (sin(dLon/2))^2
    a <- pmin(a, 1)
    2 * atan2(sqrt(a), sqrt(1 - a)) * r
}

euc <- function(x, y) (x[,1] - y[1])^2 + ((x[,2] - y[2]) * cos(y[1]))^2

