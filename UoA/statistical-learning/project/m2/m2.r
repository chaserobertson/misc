quarterly <- read.csv("Detailed Quarterly Tenancy.csv")
str(quarterly)

library(tidyverse)

q2 <- quarterly %>%
    mutate(across(str_subset(names(quarterly), 
                             regex(".Bond|(n|e).Rent|.Id")), 
                  function(x) {as.integer(gsub(',', '', x))}))
head(q2)

library(lubridate)
q3 <- q2 %>%
    mutate(date = mdy_hm(Time.Frame)) %>%
    mutate(year = year(date)) %>%
    mutate(quarter = quarter(date)) %>%
    mutate(date = paste(year, quarter, sep='-'))# %>%
    #select(-Time.Frame)
head(q3)

regional <- read.csv("rentalbond-data-regional.csv")
r2 <- regional %>%
    mutate(across(c(Lodged.Bonds, Closed.Bonds),
                  function(x) {as.integer(gsub(',', '', x))}))
r3 <- r2 %>%
    mutate(date = ymd(Time.Frame)) %>%
    mutate(year = year(date)) %>%
    mutate(month = month(date)) %>%
    select(-Time.Frame)
head(r3)

tla <- read.csv("rentalbond-data-tla.csv")

t2 <- tla %>%
    mutate(across(c(Lodged.Bonds, Active.Bonds),
                  function(x) {as.integer(gsub(',', '', x))}))
t3 <- t2 %>%
    mutate(date = ymd(Time.Frame)) %>%
    mutate(year = year(date)) %>%
    mutate(month = month(date)) %>%
    select(-c(Time.Frame, date))
head(t3)

areas <- read.csv("statsnzstatistical-area-2-2019-centroid-true-CSV/statistical-area-2-2019-centroid-true.csv")
locations <- areas %>%
    mutate(ID = SA22019_V1_00) %>%
    mutate(Location = SA22019_V1_00_NAME) %>%
    select(c(ID, Location))
locations <- rbind(locations, list(-99, 'ALL'))
tail(locations)

q.df <- left_join(q3, locations, by=c('Location.Id' = 'ID'))
head(q.df)
r.df <- r3
t.df <- t3

library(ggplot2)
library(viridis)

q.df %>%
    filter(Location == 'ALL', Dwelling.Type == 'ALL', Number.Of.Beds == 'ALL', year > 2013) %>%
    ggplot(aes(x=quarter, y=Total.Bonds, colour=factor(quarter))) +
    facet_grid(~year) +
    geom_point(size=2) + 
    scale_color_viridis(discrete=T) +
    theme_minimal()

q.df %>%
    filter(Location == 'ALL', Dwelling.Type == 'ALL', Number.Of.Beds == 'ALL', year > 2012) %>%
    ggplot(aes(x=quarter, y=Active.Bonds, colour=factor(quarter))) +
    facet_grid(~year) +
    geom_point(size=2) + 
    scale_color_viridis(discrete=T) +
    theme_minimal()

q.df %>%
    filter(Location == 'ALL', Dwelling.Type == 'ALL', Number.Of.Beds == 'ALL', year > 2013) %>%
    ggplot(aes(x=quarter, y=Closed.Bonds, colour=factor(quarter))) +
    facet_grid(~year) +
    geom_point(size=2) + 
    scale_color_viridis(discrete=T) +
    theme_minimal()

q.type = q.df %>%
    filter(Location == 'ALL', Dwelling.Type == 'ALL', 
           Number.Of.Beds == 'ALL', year > 2013) %>%
    pivot_longer(c(Total.Bonds, Closed.Bonds), 
                 names_to="Bond.Type", values_to="Bond.Number") %>%
    group_by(year, Bond.Type) %>%
    summarise(Annual.Sum = sum(Bond.Number))

q.type %>%
    ggplot(aes(x=year, y=Annual.Sum, colour=Bond.Type)) +
    geom_line() +
    scale_colour_viridis(discrete=T) +
    theme_minimal() +
    labs(title="Total Annual Bonds Per Year, by Type")

q.building = q.df %>%
    filter(Location == 'ALL', Number.Of.Beds == 'ALL', year > 2012) %>%
    pivot_longer(c(Total.Bonds, Closed.Bonds), 
                 names_to="Bond.Type", values_to="Bond.Number") %>%
    group_by(year, Bond.Type, Dwelling.Type) %>%
    summarise(Annual.Sum = sum(Bond.Number))

q.building %>%
    ggplot(aes(x=year, y=Annual.Sum, colour=Bond.Type)) +
    facet_wrap(~Dwelling.Type, scales="free") +
    geom_line() +
    scale_colour_viridis(discrete=T) +
    theme_minimal()

r.loc = r.df %>%
    filter(Location.Id > 0, year > 2013, year < 2022) %>%
    pivot_longer(c(Lodged.Bonds, Closed.Bonds), 
                 names_to="Bond.Type", values_to="Bond.Number") %>%
    group_by(year, Bond.Type, Location) %>%
    summarise(Annual.Sum = sum(Bond.Number))


r.loc %>%
    ggplot(aes(x=year, y=Annual.Sum, colour=Bond.Type)) +
    facet_wrap(~Location, scales="free") +
    geom_line() +
    scale_colour_viridis(discrete=T) +
    theme_minimal()

r.time = r.df %>%
    filter(Location.Id > 0, year > 2017, year < 2022) %>%
    pivot_longer(c(Median.Rent, Upper.Quartile.Rent, Lower.Quartile.Rent), 
                 names_to="Type", values_to="Value") %>%
    group_by(year, Type, Location) %>%
    summarise(Annual.Mean = mean(Value))

r.time %>%
    ggplot(aes(x=year, y=Annual.Mean, colour=Type)) +
    facet_wrap(~Location, scales="free") +
    geom_line() +
    scale_colour_viridis(discrete=T) +
    theme_minimal()


