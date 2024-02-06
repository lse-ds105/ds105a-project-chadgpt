library(ggplot2)
library(tidyverse)
library(ggradar)

df <- read_csv("./data/top10cuisines_nutrients_normalised.csv")
print(df)

# Create a radar plot
plot <- df %>%
    ggradar( 
    font.radar = 'roboto',
    grid.label.size = 1,
    axis.label.size = 5, # Afftects the names of the variables
    group.point.size = 1   # Simply the size of the point
    )

# Save the plot
ggsave(plot, filename = "./plots/nutrients_radar_plot.png", width = 16, height = 9, units = "in", dpi = 600)
