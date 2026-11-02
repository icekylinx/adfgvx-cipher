CC ?= cc
CFLAGS ?= -O3 -std=c11 -Wall -Wextra
LDLIBS ?= -lm

PROGRAMS = segmentation_rank segmentation_profile_batch subsolve_marginal \
           pair_marginal anchored_joint joint_domain_subsolve6 pair_order_rank
BINARIES = $(addprefix bin/,$(PROGRAMS))

.PHONY: all check clean
all: $(BINARIES)

bin/%: src/%.c src/sixgram_model.h
	mkdir -p bin
	$(CC) $(CFLAGS) $< $(LDLIBS) -o $@

check: all
	python3 tools/verify_cases.py
	python3 tools/verify_cli.py

clean:
	rm -f $(BINARIES)
