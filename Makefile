proto-gen: copy-proto-files
	./scripts/protocgen.sh

copy-proto-files:
	@rm -rf nibiru/proto
	@rm -rf proto/

	@mkdir -p proto/
	@cp -r ../nibiru/proto/ ./
