library(ggplot2)
library(tidyverse)
library(ggradar)

df <- read_csv("./data/top10cuisines_nutrients_normalised.csv")
print(df)

for (i in colnames(df)[2:ncol(df)]) {
    selected_df <- 
        df %>%
        select(c("cuisine", i)) %>%
        ggradar(
            plot.title = paste("Nutrient Profile of", i, "Cuisine"),
            font.radar = 'roboto',
            values.radar = c(0, 5, 10),
            grid.label.size = 5,
            axis.label.size = 5, # Afftects the names of the variables
            group.point.size = 2,   # Simply the size of the points
            gridline.min.linetype = 2,
            gridline.mid.linetype = 1,
            gridline.max.linetype = 1,
        ) %>%
        ggsave(filename = paste0("./plots/", i, "_radar_plot.png"), width = 16, height = 9, units = "in", dpi = 600)
}
# Create a radar plot
# plot <- df %>%
#     ggradar(
#     plot.title = "Nutrient Profiles of Top 10 Most Popular Cuisines",
#     font.radar = 'roboto',
#     legend.title = "Cuisine",
#     values.radar = c(0, 5, 10),
#     grid.label.size = 5,
#     axis.label.size = 5, # Afftects the names of the variables
#     group.point.size = 2,   # Simply the size of the points
#     gridline.min.linetype = 2,
#     gridline.mid.linetype = 1,
#     gridline.max.linetype = 1,
#     )

# # Save the plot
# ggsave(plot, filename = "./plots/nutrients_radar_plot.png", width = 16, height = 9, units = "in", dpi = 600)
