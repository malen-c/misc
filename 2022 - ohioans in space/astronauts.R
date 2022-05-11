library(tidyverse)

#reading in data
astros <- read.csv('data/astros.csv') %>%
  replace_na(list('ohio' = 0)) %>%
  group_by(year) %>%
  mutate(oh_astro = sum(ohio), non_oh_astro = n() - oh_astro) %>%
  select(-name, -ohio) %>%
  distinct(.keep_all = TRUE)

#creating "expected" birth counts, which are simply the values of astronauts
#from ohio we would expect each year if the amount of astronauts born in a year was
#fixed and the amount of astronauts from ohio was the proportion of people born
#in ohio vs. rest of US that year times the total amount of astronauts born

birth <- read.csv('data/birth.csv') %>%
  right_join(astros) %>%
  mutate(expected_oh_astro = (oh_birth/birth) * (non_oh_astro + oh_astro))

#observed stat in question is the difference in means between the true amount of
#ohio astronauts born vs. the expected amount of ohio astronauts born for all
#years from 1921-1978

obs_stat <- mean(birth$oh_astro - birth$expected_oh_astro)

#total amounts of astros every year
yearly_astros <- birth$oh_astro + birth$non_oh_astro
#proportion of people born in Ohio vs. rest of US every year
ohio_birth_prop <- birth$oh_birth/birth$birth

#creating null distribution which is a million trials of binomial simulations
#with amount of astros born each year being the size of the trial, ohio birth
#prop being the probability for each trial
set.seed(10)
null_dist <- mapply(rbinom, 10^6, yearly_astros, ohio_birth_prop)

#calculating stat of interest for each replicate
null_stats <- 
  data.frame(replicate = 1:10^6,
             stat = rowMeans(null_dist) - mean(birth$expected_oh_astro))

ggplot(null_stats, aes(x = stat)) +
  geom_histogram(color = 'white', fill = 'midnight blue') +
  geom_vline(xintercept = obs_stat, color = 'red', lwd = 2) +
  scale_y_continuous(expand = c(0,0), limits = c(0, 200000)) +
  scale_x_continuous(expand = c(0,0)) +
  labs(title = 'Null Dist. of Mean Difference Between True and Expected Ohio Astronauts Born per Year')

#one sided p-value is 0.114439, probably just a coincidence!
filter(null_stats, stat >= obs_stat) %>%
  nrow()/10^6
