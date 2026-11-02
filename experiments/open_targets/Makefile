CC ?= cc
CFLAGS ?= -O3 -std=c11
LDLIBS = -lm
ENGINES = gap_anchored sparse_loss group_transfer segment_gap refine_segments relabel_rows_columns component_sixgram
BINS = $(addprefix bin/,$(ENGINES))

.PHONY: all clean
all: $(BINS)

bin:
	mkdir -p bin

bin/%: %.c | bin
	$(CC) $(CFLAGS) $< $(LDLIBS) -o $@

bin/sparse_loss: gap_anchored.c
bin/component_sixgram: ../joint_search/src/sixgram_model.h

clean:
	rm -f $(BINS)
