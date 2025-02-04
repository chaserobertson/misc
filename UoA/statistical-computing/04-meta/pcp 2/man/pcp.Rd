\name{pcp}
\alias{pcp}
\title{
Parallel Coordinate Plot
}
\description{
Plots any convertible list of variables as a series of configurable lines between each observation's [0,1] normalised values. 
}
\usage{
pcp(data, col = 2, lwd = 1, lty = 1, ...)
}
\arguments{
  \item{data}{
A list whose 2 or more items' coordinating values will be parallel plotted.
Item vectors must be finite numeric, or convertible to finite numeric via factor/integer.
}
  \item{col}{
Color(s) to use for each coordinate line.
}
  \item{lwd}{
Line width(s) to use for each coordinate line.
}
  \item{lty}{
Line type(s) to use for each coordinate line.
}
  \item{\dots}{
Further graphical parameters to be passed to \code{graphics::matplot(...)}
}
}
\value{
Returns a [0,1] normalised matrix constructed from argument \code{data}, with each list item from \code{data} as a named column. Character or factor type list items from \code{data} are cast to numeric with base \code{as.type(x)} methods.
}
\author{
Chase Robertson, University of Auckland
}
\examples{
# basic usage
pcp(iris, col=iris$Species)

# can convert character-type vectors and/or recycle values
recycled <- list(x=0, y=1:2, z=c("a", "b", "c"))
pcp(recycled, col=1:3, lty=1:3, lwd=1:3)

# further graphical parameters passed to graphics::matplot
with_params <- list(x=1:12, y=month.abb, z=12:1)
pcp(with_params, cex=2, ylim=c(-1, 2), add=FALSE)
}