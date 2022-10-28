p    = python3
main = main.py
runtime = bun
file = $(call args)
args = $(filter-out $@,$(MAKECMDGOALS))

bun:
	time $(p) $(main) -f $(file) -bun

deno:
	time $(p) $(main) -f $(file)

dir:
	time $(p) $(main) -d $(file)

dir-run: 
	$(dir)
	time $(runtime) run "output/$(file).ts"

%:
    @:
