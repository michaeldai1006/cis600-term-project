#
# John D'Amaro
# CIS 600 - Social Media Mining Final Project
# Word Cloud Visualizations
#

install.packages("wordcloud")
install.packages("stringr")
library(stringr)
library(wordcloud)
library(RColorBrewer)

setwd("C:\\Users\\user\\Desktop\\CIS600TermProject\\Data Storage\\Data\\")

day.data <- read.csv(paste0("18April.csv")
                    , header = TRUE
                    , stringsAsFactors = FALSE)

## Data Cleaning
day.data$Hashtag[day.data$Hashtag == "COVIDãf¼19"] <- "COVID--19"
day.data$TweetDate <- as.Date(day.data$TweetDate)

## Order Data by Hashtag Frequency
day.data <- day.data[order(day.data$HashtagFreq, decreasing = TRUE), ]

## Removing data points with low frequency
zap <- which(day.data$HashtagFreq < 5)
day.data <- day.data[-zap, ]

## Scale
day.data$HashtagFreq <- day.data$HashtagFreq^(1/2.5)

## Wordcloud Plot
par(mar = c(0,0,0,0), bg = "black")
myPalFun <- colorRampPalette(
            c("chartreuse2", "deepskyblue", "forestgreen")
            , bias = 2)
wordcloud(day.data$Hashtag, freq = day.data$HashtagFreq
          , min.freq = 1, scale = c(4,0.6)
          , max.words = Inf, random.order = F
          , ordered.colors = T, rot.per = 0.15, 
          , colors = myPalFun(length(day.data$HashtagFreq)))

## c("chartreuse2", "deepskyblue", "forestgreen")
## color palette everyone likes
