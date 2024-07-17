library(optparse)
library(tidyverse)

option_list <- list(
  make_option(c("-g", "--gtf"), type="character", default=NULL,
              help="GTF file path", metavar="file"),
  make_option(c("-t", "--tsv"), type="character", default=NULL,
              help="TSV file path", metavar="file"),
  make_option(c("-o", "--output"), type="character", default="output",
              help="Output prefix for TSV files", metavar="prefix")
)

# Parse options
opt <- parse_args(OptionParser(option_list=option_list))

# Validate inputs
if (is.null(opt$gtf) || is.null(opt$tsv)) {
  stop("Error: Both --gtf and --tsv must be specified\n", call. = FALSE)
}

# create a function to parse the attributes column of the GTF file
parse_attributes <- function(attribute_string) {
  key_value_pairs <- str_extract_all(attribute_string, "\\w+ \\\"[^\\\"]+\\\"")[[1]]
  keys <- str_extract(key_value_pairs, "^\\w+")
  values <- str_extract(key_value_pairs, "\\\"[^\\\"]+\\\"") %>% str_remove_all("\"")
  set_names(values, keys)
}

# Read and parse GTF data
gtf_data <- read_tsv(opt$gtf, col_types = cols(.default = "c"), col_names = FALSE) %>%
  mutate(across(everything(), as.character)) %>%
  rowwise() %>%
  mutate(attributes = list(parse_attributes(X9))) %>%
  unnest_wider(col = attributes) %>%
  select(-X9) %>%
  rename(seqname = X1, source = X2, feature = X3, start = X4, end = X5, 
         score = X6, strand = X7, frame = X8)

# Read in TSV file that contains information about the transcript type and the ORF annotation type.
# The annotation types are: antisense, bidirectional_promoter_lncRNA, cds, cds-intergenic, 
# cds-intronic, cds-utr3, intergenic, intronic, ncRNA, nmd, pseudogene, retained_intron,
# utr3, utr3-intergenic, utr3-intronic, utr5, utr5-cds, utr5-intergenic, utr5-intronic


tsv_data <- read_tsv(opt$tsv) %>%
  janitor::clean_names() %>%
  rename(orf_annotation = or_fannotation)

combined_data <- left_join(tsv_data, gtf_data, by = c("novel_orf_id" = "gene_id"))

write_tsv(combined_data, paste0(opt$output, "_full.tsv"))
write_tsv(select(combined_data, novel_orf_id, AA_seq), paste0(opt$output, "_amino_acid.tsv"))