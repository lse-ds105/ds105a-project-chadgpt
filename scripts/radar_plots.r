'''
This script generates radar plots for each cuisine in the dataset.
This script uses the ggradar package to generate the radar plots, which is based off ggplot2.
Run install.packages("ggradar") to install the ggradar package.
'''

library(ggplot2)
library(tidyverse)
library(ggradar)

df <- read_csv("../data/top10cuisines_nutrients_normalised.csv", trim_ws = FALSE)
print(df$cuisine)

for (i in df$cuisine) {
    selected_df <- 
        df %>%
        filter(cuisine == i | cuisine == " healthy threshold") %>%
       arrange(cuisine != " healthy threshold")
    plot <- selected_df %>%
        ggradar(
group.colours = c("#858585", "#5C3DA4"),
           base.size = 8,
            plot.title = paste0("Nutrient Profile of ", i, " Cuisine"),
            font.radar = 'roboto',
            values.radar = c(0, 5, 10),
            grid.label.size = 5,
            axis.label.size = 6, # Affects the names of the variables
            group.line.width = 1,
            group.point.size = 2,   # size of the the points
            gridline.min.linetype = 1,
            gridline.mid.linetype = 2,
            gridline.max.linetype = 1,
           legend.position = "top"
        ) %>%
        ggsave(filename = paste0("../docs/plots/radar_plot_", i, ".png"), width = 8, height = 8, units = "in", dpi = 600)
print(paste0("../docs/plots/radar/radar_plot_", i, ".png"))
}