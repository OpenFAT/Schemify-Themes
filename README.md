# Schemify-Themes

Colour presets for [Schemify](https://github.com/OpenFAT/Schemify). A preset is a `.records` file of `style` overrides layered over Schemify's base `ui/default-plugin/ui.records`, with the last value winning. It changes colours, borders and spacing only. Nodes, keys and accelerators stay as they are.

| Theme | File |
|---|---|
| Modern (dark chrome, dark and light canvas) | [themes/modern.records](themes/modern.records) |

## The gate

Every preset must pass the colour checks of Schemify's `schemify-theme` skill: circuit-layer contrast, grid contrast, highlight separation under deutan and protan simulation, chrome text contrast and the accent budget.

```sh
curl -fsSL -o ui.records https://raw.githubusercontent.com/OpenFAT/Schemify/main/ui/default-plugin/ui.records
python3 tools/check_theme.py ui.records themes/modern.records
```

CI runs this check on every file in `themes/`. The rules and the baseline palette are in [Schemify's theme skill](https://github.com/OpenFAT/Schemify/blob/main/docs/dev/skills/schemify-theme/SKILL.md). `tools/check_theme.py` is a copy of that skill's checker; when Schemify changes `HILITE_LAYERS`, copy the checker again.

## Adding a theme

Copy `themes/modern.records`, then change the colour values. Keep every layer role's meaning the same (see the skill). Run the gate, then open a pull request.
