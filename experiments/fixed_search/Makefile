CC ?= cc
CFLAGS ?= -O3 -std=c11 -Wall -Wextra -Wno-unused-function
LDLIBS ?= -lm
PROGRAMS = subsolve marginal_subsolve marginal_subsolve6 dictionary_profile

.PHONY: all check clean
all: $(addprefix bin/,$(PROGRAMS))
bin/%: src/%.c src/sixgram_model.h
	mkdir -p bin
	$(CC) $(CFLAGS) $< $(LDLIBS) -o $@
check: all
	python3 tools/verify_inputs.py
clean:
	rm -f $(addprefix bin/,$(PROGRAMS))
