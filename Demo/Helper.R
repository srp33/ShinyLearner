make_faceted_point_plot = function(plot_data, x, y, ylab, palette, 
                                   facet_column, out_file_path, base_size=13,
                                   y_lines=NULL, facet_scales="fixed", ncol=2) {
  p = ggplot(plot_data, aes_string(x = x, y = y, color=x))

  if (!is.null(y_lines)) {
    for (y_line in y_lines)
      p = p + geom_hline(yintercept = y_line, col="black", linetype="dotted")
  }
    
  p = p + geom_point(size=2) +
    coord_flip() +
    ylab(ylab) +
    scale_color_manual(values=palette) +
    scale_x_discrete(limits=rev(levels(pull(plot_data, x)))) +
    theme_bw(base_size=base_size) +
    theme(axis.title.y = element_blank(),
          axis.text.y = element_blank(),
          axis.ticks.y = element_blank(),
          panel.spacing.x = unit(1, "lines"),
          strip.background = element_blank(),
          strip.placement = "outside",
          strip.text = element_text(face="bold")) +
    facet_wrap(paste0("~", facet_column), ncol=ncol, scales=facet_scales)
  
  print(p)
  
  ggsave(out_file_path, width=dimension_1, height=dimension_2)
}

make_bar_plot = function(plot_data, x, y, xlab, ylab, out_file_path, base_size=18, axis_label_angle=40) {
  p = ggplot(plot_data, aes_string(x = x, y = y)) +
    geom_col() +
    coord_flip() +
    labs(x = xlab,
         y = ylab) +
    scale_x_discrete(limits=rev(levels(pull(plot_data, x)))) +
    theme_bw(base_size=base_size) +
    theme(axis.title.x = element_text(margin = margin(t = 10, r = 0, b = 0, l = 0))) +
    theme(axis.title.y = element_text(margin = margin(t = 0, r = 10, b = 0, l = 0)))
#    theme(axis.text.x = element_text(angle = axis_label_angle, hjust = 1))
  
  print(p)

  ggsave(out_file_path, width=dimension_2, height=dimension_1)
}

make_algo_comparison_plot = function(metrics_data, algo1, algo2, out_file_path, base_size=18) {
  plot_data = filter(metrics_data, Algorithm %in% c(algo1, algo2)) %>%
    group_by(Description, Algorithm) %>%
    summarize(AUROC=median(Value)) %>%
    spread(Algorithm, AUROC) %>%
    rename(x=algo1) %>%
    rename(y=algo2)

  x = pull(plot_data, x)
  y = pull(plot_data, y)
  coef = cor(x, y)
  
  p = ggplot(plot_data, aes(x, y)) +
    geom_point(size=3) +
    geom_abline(slope=1, intercept = 0, color="gray70", linetype="dashed", size=1.2) +
    xlab(algo1) +
    ylab(algo2) +
    xlim(0.5, 1) +
    ylim(0.5, 1) +
    ggtitle(paste0("r = ", round(coef, 2))) +
    theme_bw(base_size=base_size) +
    theme(plot.title = element_text(hjust = 0.5))
  
  print(p)
  
  ggsave(out_file_path, width=dimension_1, height=dimension_1)
}

make_continuous_heatmap = function(plot_data, x, y, fill_column, xlabel, ylabel, legend_title, out_file_path, base_size=18, keep_x_axis=TRUE, fill_values_range=c(-1, -0.5, 0, 0.5, 1), reverse_colors=FALSE) {
  palette = c("#d7191c", "#fdae61", "#ffffbf", "#abd9e9", "#2c7bb6")
  
  if (reverse_colors)
    palette = rev(palette)
  
  p = ggplot(plot_data, aes_string(x = x, y = y)) +
    geom_tile(aes_string(fill=fill_column), color="white") +
    scale_fill_gradientn(name=legend_title, colours = palette, trans="reverse", values=fill_values_range) +
    xlab(xlabel) +
    ylab(ylabel) +
    scale_y_discrete(limits=rev(levels(pull(plot_data, y)))) +
    theme_bw(base_size=base_size) +
    theme(axis.text.x=element_text(angle=40, hjust=1),
          panel.grid.major = element_blank(),
          panel.grid.minor = element_blank())
  
  if (is.null(legend_title))
    p = p + guides(fill=FALSE)
  
 if (!keep_x_axis)
   p = p + theme(axis.text.x=element_blank(),
                 axis.ticks.x=element_blank())

  print(p)

  ggsave(out_file_path, width=dimension_2, height=dimension_1)
}

make_diff_bar_plot = function(plot_data, x, y, fill_column, facet_column, xlab, ylab, out_file_path) {
  colors = c("#de77ae", "#7fbc41")
  
  p = ggplot(plot_data, aes_string(x=x, y=y)) +
    geom_col(aes_string(fill=fill_column)) +
    scale_fill_manual(values=colors) +
    geom_hline(yintercept = 0) +
    facet_wrap(paste0("~", facet_column), ncol=2, scales="fixed") +
    xlab(xlab) +
    ylab(ylab) +
    guides(fill=FALSE) +
    theme_bw(base_size=13) +
    theme(axis.text.x = element_text(angle = 60, hjust = 1))
  
  print(p)
  
  ggsave(out_file_path, width=dimension_1, height=dimension_2)
}

make_param_box_plot = function(plot_data, x, y, ylab, xlab=NULL, base_size=13) {
  p = ggplot(plot_data, aes_string(x=x, y=y)) +
    geom_boxplot(outlier.shape = NA) +
    geom_jitter() +
    xlab(xlab) +
    ylab(ylab) +
    theme_bw(base_size=base_size)
  
  return(p)
}