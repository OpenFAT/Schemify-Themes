#!/usr/bin/env bash
# Builds the guest for wasm32-unknown-unknown into schemify_themes.wasm at the repository root
# (committed: `schemify pack` installs it). Host paths are remapped out of the module, so the bytes
# depend only on the sources, Cargo.lock and the toolchain.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export CARGO_ENCODED_RUSTFLAGS="--remap-path-prefix=$here=/schemify-themes"$'\x1f'"--remap-path-prefix=${CARGO_HOME:-$HOME/.cargo}=/cargo"
cargo build --manifest-path "$here/Cargo.toml" --release --target wasm32-unknown-unknown
wasm="${CARGO_TARGET_DIR:-$here/target}/wasm32-unknown-unknown/release/schemify_themes.wasm"
size=$(wc -c <"$wasm")
(( size < 200 * 1024 )) || { echo "error: schemify_themes.wasm is $size bytes (limit 200 KB)" >&2; exit 1; }
cp "$wasm" "$here/schemify_themes.wasm"
