library(ggplot2)
library(tidyverse)
library(ggradar)

df <- read_csv("./data/top10cuisines_nutrients_normalised.csv")
print(df)

for (i in df$cuisine) {
    selected_df <- 
        df %>%
        filter(cuisine == i)
    plot <- selected_df %>%
        ggradar(
            plot.title = paste0("Nutrient Profile of ", i, "Cuisine"),
            font.radar = 'roboto',
            values.radar = c(0, 5, 10),
            grid.label.size = 5,
            axis.label.size = 5, # Affects the names of the variables
            group.line.width = 1,
            group.point.size = 2,   # Simply the size of the points
            gridline.min.linetype = 1,
            gridline.mid.linetype = 2,
            gridline.max.linetype = 1
        ) %>%
        ggsave(filename = paste0("./plots/radar/radar_plot_", i, ".png"), width = 8, height = 8, units = "in", dpi = 600)
}