
# Change Log

All notable changes to this project will be documented in this file.

## [Unreleased](https://github.com/NibiruChain/py-sdk/compare/v0.3.0...HEAD)

- ...

## [v0.4.0](https://github.com/NibiruChain/py-sdk/releases/tag/v0.4.0) 2022-09-06

### Improvements

- [[#117]](https://github.com/NibiruChain/py-sdk/pull/117) feat: add websocket module to py-sdk
- [[#122]](https://github.com/NibiruChain/py-sdk/pull/122) feat: get block by height  enhancement
- [[#126]](https://github.com/NibiruChain/py-sdk/pull/126) feat (rpc): add more chain info queries
- [[#127]](https://github.com/NibiruChain/py-sdk/pull/127) feat: add generator for blocks queries

## [v0.3.0](https://github.com/NibiruChain/py-sdk/releases/tag/v0.3.0) 2022-08-25

### API Breaking Changes

- [[#111]](https://github.com/NibiruChain/nibiru-py/pull/111) case str to float safely in the vpool module's all pools query.

## [v0.2.0](https://github.com/NibiruChain/py-sdk/releases/tag/v0.2.0) [2022-08-24](https://github.com/NibiruChain/py-sdk/pull/109)

### API Breaking Changes

- [[#109]](https://github.com/NibiruChain/nibiru-py/pull/109) Update nibiru-proto dependency for v0.14.0 binary.
- [[#108]](https://github.com/NibiruChain/py-sdk/pull/108) Improve query error handling
- [[#103]](https://github.com/NibiruChain/py-sdk/pull/103) hotfix/test(query_clients): Test vpool.query.all_pools fn. Account for deserialize edge case #102.
- [[#96]](https://github.com/NibiruChain/py-sdk/pull/96) feat: Split the design of txs between message and execution.

### Improvements

- [[#104]](https://github.com/NibiruChain/py-sdk/pull/104) docs: Update README.md
- [[#97]](https://github.com/NibiruChain/py-sdk/pull/97) Remove legacy run-examples.sh
- [[#96]](https://github.com/NibiruChain/py-sdk/pull/96) refactor(ci-cd): Update linter workflow. Cache poetry installation.
- [[#96]](https://github.com/NibiruChain/py-sdk/pull/96) test: Add back utils_test file

## [v0.1.0](https://github.com/NibiruChain/py-sdk/releases/tag/v0.1.0)  2022-08-22

- [[#81]](https://github.com/NibiruChain/py-sdk/pull/81) feat(proto): use external proto pkg `nibiru_proto` for versioned types
- [[#103]](https://github.com/NibiruChain/py-sdk/pull/103) fix(query_clients): account for missing fields on the pb_msg in deserialize
- [[#103]](https://github.com/NibiruChain/py-sdk/pull/103) test(vpool): test_query_vpool_base_asset_price
- [[#98]](https://github.com/NibiruChain/py-sdk/pull/98) chore: Remove protogen script as we're pulling from `nibiru-proto` now
- [[#100]](https://github.com/NibiruChain/py-sdk/pull/100) chore: Automate publishing with ci
- [[#92]](https://github.com/NibiruChain/py-sdk/pull/92) refactor: Split the design of tx between message and execution

## v0.0.17 - 2022-08-16

- hotfix: fix the json parse for grpc error by @matthiasmatt in [#75](https://github.com/NibiruChain/py-sdk/pull/75)
- fix: Revert "Lint github action" by @Unique-Divine in [#68](https://github.com/NibiruChain/py-sdk/pull/68)
- test: refactored perp and price feed tests by @onikonychev in [#73](https://github.com/NibiruChain/py-sdk/pull/73)
- test: Add unit tests for perp queries and txs by @matthiasmatt in [#54](https://github.com/NibiruChain/py-sdk/pull/54)
- dev: Lint github action by @onikonychev in [#66](https://github.com/NibiruChain/py-sdk/pull/66)
- dev: Linting action and pre-commit by @onikonychev in [#72](https://github.com/NibiruChain/py-sdk/pull/72)
- docs: Add sdk doc (network, txconfig and sdk) by @matthiasmatt in [#69](https://github.com/NibiruChain/py-sdk/pull/69)
- docs: README update by @onikonychev in [#74](https://github.com/NibiruChain/py-sdk/pull/74)

## v0.0.16 - 2022-08-14

For NibiruChain/nibiru binary version v0.12.1-alpha

* [#65](https://github.com/NibiruChain/nibiru-py/pull/65) - fix: open/get position deserialization

## v0.0.15 - 2022-08-12

* [#50](https://github.com/NibiruChain/nibiru-py/pull/50) - Rename classnames and variables

## v0.0.14.a1 - 2022-08-13

Note that you now install the [`nibiru` package](https://pypi.org/project/nibiru/) with `pip install nibiru`.

### Improvements

* chore: Update package version to v0.0.14.a1 by @NibiruHeisenberg in https://github.com/NibiruChain/nibiru-py/pull/59
* [#46](https://github.com/NibiruChain/nibiru-py/pull/46) - Bugfix in query perp trader position
* test,ci,feat: (1) Use poetry for pkg management. (2) Improve CI. (3) Re-gen protos for v0.12.1-alpha of nibiru by @Unique-Divine in https://github.com/NibiruChain/nibiru-py/pull/53
* docs(README): Documented entire development setup. Fixed badges. Added installation instructions for pyenv, poetry, pip by @Unique-Divine in https://github.com/NibiruChain/nibiru-py/pull/55

### Fixes

* refactor: fix protogen script by @NibiruHeisenberg in https://github.com/NibiruChain/nibiru-py/pull/49
* Removed manual position deserialization by @onikonychev in https://github.com/NibiruChain/nibiru-py/pull/47
* Revert "Removed manual position deserialization" by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/48
* fix: Fix protogen script, upgraded proto  by @NibiruHeisenberg in https://github.com/NibiruChain/nibiru-py/pull/44
* Bugfix in query perp trader position by @onikonychev in https://github.com/NibiruChain/nibiru-py/pull/46

## v0.0.14 - 2022-08-11

- Upgraded proto to fit nibiru chain v0.12.2
- Simplified Makefile
- Fixed Protogen script

## v0.0.1 through v0.0.13

* Change the link of the conf.py file by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/43
* Add readthedoc configuration for autodoc by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/42
* Mat/more doc by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/41
* Add documentation and improve the output of the dex queries by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/40
* ci,tests: Verify the SDK works with tests and set up GHA workflow to build and run from scratch  by @Unique-Divine in https://github.com/NibiruChain/nibiru-py/pull/38
* Mat/autodoc by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/37
* Qol improvements by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/35
* Updated references to old repo name in https://github.com/NibiruChain/nibiru-py/pull/32
* Fix some issues with the rst files by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/34
* Add documentation on the nibiru perp by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/33
* Cleanup in https://github.com/NibiruChain/nibiru-py/pull/26
* Bump version to 0.0.11 to deploy Pypi by @onikonychev in https://github.com/NibiruChain/nibiru-py/pull/31
* feat: Add documentation by @matthiasmatt in https://github.com/NibiruChain/nibiru-py/pull/29
* Changed network default to secure in https://github.com/NibiruChain/nibiru-py/pull/30
* Removed auto cosmInt transformation from response in https://github.com/NibiruChain/nibiru-py/pull/28
* Added testnet and removed cookie code in https://github.com/NibiruChain/nibiru-py/pull/27
* Fixed paths in run script and added some info to README in https://github.com/NibiruChain/nibiru-py/pull/25
* Added pricefeed module in https://github.com/NibiruChain/nibiru-py/pull/23
* Added testnet network in https://github.com/NibiruChain/nibiru-py/pull/22
* Fixed float to int cast in https://github.com/NibiruChain/nibiru-py/pull/21
* Fixed sdk types and examples in https://github.com/NibiruChain/nibiru-py/pull/20
* Bumped version to release in https://github.com/NibiruChain/nibiru-py/pull/19
* Fixed error in https://github.com/NibiruChain/nibiru-py/pull/18
* Updated protos and fixed property names to snake_case in https://github.com/NibiruChain/nibiru-py/pull/17
* Fixed network assignment in https://github.com/NibiruChain/nibiru-py/pull/16
* Added vpool and removed async/await in https://github.com/NibiruChain/nibiru-py/pull/15
* Github workflow: do release on master merge by @onikonychev in https://github.com/NibiruChain/nibiru-py/pull/11
* Disabled cron job to sync timeout height in https://github.com/NibiruChain/nibiru-py/pull/10
* Changed tx default to async and leave sequence count in case of tx err in https://github.com/NibiruChain/nibiru-py/pull/9
* Added tx type option to sdk wrapper in https://github.com/NibiruChain/nibiru-py/pull/8
* Rethrow sim err and allow multiple msgs in tx in https://github.com/NibiruChain/nibiru-py/pull/7
* Refactored to use new sdk wrapper and cleanup in https://github.com/NibiruChain/nibiru-py/pull/6
* Added wrapper to simplify usage in https://github.com/NibiruChain/nibiru-py/pull/5
* Added pyi (type info) to generated protos + minor cleanup in https://github.com/NibiruChain/nibiru-py/pull/3
