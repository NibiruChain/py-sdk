proto-gen: copy-proto
	./scripts/protocgen.sh

copy-proto:
	@rm -rf nibiru/proto
	@mkdir -p proto/
	@cp -r ../nibiru/proto/ proto/