library(plyr)
library(ggplot2)

# Load the data from file.
data <- read.csv('~/src/scotus-predict/model_output/20140515200540/justice_outcome_data.csv')

# Generate the justice-year average accuracies and use post-1953 rows.
year_data <- ddply(data, c("justice", "year"), function(X) mean(X$correct=="True"))
year_data <- year_data[year_data$year>=1953, ]

# Cleanup the justice names for display.
year_data$justice_name <- revalue(as.character(year_data$justice),
    c('78'='Black',
      '79'='Reed',
      '80'='Frankfurter',
      '81'='Douglas',
      '84'='Jackson',
      '86'='Burton',
      '88'='Clark',
      '89'='Minton',
      '90'='Warren',
      '91'='Harlan',
      '92'='Brennan',
      '93'='Whittaker',
      '94'='Stewart',
      '95'='White',
      '96'='Goldberg',
      '97'='Fortas',
      '98'='Marshall',
      '99'='Burger',
      '100'='Blackmun',
      '101'='Powell',
      '102'='Rehnquist',
      '103'='Stevens',
      '104'='O\'Connor',
      '105'='Scalia',
      '106'='Kennedy',
      '107'='Souter',
      '108'='Thomas',
      '109'='Ginsburg',
      '110'='Breyer',
      '111'='Roberts',
      '112'='Alito',
      '113'='Sotomayor',
      '114'='Kagan'))

# Reorder by year.
year_data$justice_name <- as.character(year_data$justice_name)
year_data$justice_name <- factor(year_data$justice_name, levels=unique(year_data$justice_name))

# Generate a full heatmap.
scotusheatmap_final <- ggplot(year_data, aes(year, justice_name)) +
    geom_tile(aes(fill = year_data$V1), colour="grey") +
    scale_fill_continuous(low="#ece7f2", high="#2b8cbe", na.value="#333333") +
    scale_x_continuous(name="Year", breaks=c(1953,1963,1973,1983,1993,2003,2013)) +
    scale_y_discrete(name="Justice") + 
    theme(legend.title=element_blank()) +
    theme(panel.background=element_blank())

# Review the final product.
scotusheatmap_final

# Save to file.
ggsave(filename = "scotus_heatmap_final.png", plot = scotusheatmap_final, width=20, height=12)