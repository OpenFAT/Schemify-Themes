# Schemify-Themes

The [spicetify-themes](https://github.com/spicetify/spicetify-themes) catalogue for [Schemify](https://github.com/OpenFAT/Schemify): 15 themes and 115 colour schemes, each recoloring the editor's chrome and the schematic canvas. Pick one from **View → Themes**.

![View → Themes in Schemify](screenshots/menu.png)

## Install

Add the plugin to your `init.lua`, then run `schemify pack sync`:

```lua
schemify.pack.add {
  { src = "https://github.com/OpenFAT/Schemify-Themes.git" },
}
```

Choose a theme from **View → Themes → *theme* → *scheme***, or run its command (listed under each screenshot below). **Schemify default** returns to the editor's own look.

### Keep a theme across restarts

The plugin does not remember your choice. To start with a theme, load the plugin on that theme's command and run the command at startup:

```lua
schemify.pack.add {
  { src = "https://github.com/OpenFAT/Schemify-Themes.git", lazy = { cmd = "theme.sleek.nord" } },
}
schemify.cmd("theme.sleek.nord")
```

## How the themes are made

A spicetify scheme is a list of named colours for Spotify (`main`, `sidebar`, `card`, `text`, `subtext`, `button`, and so on). [`tools/spicetify.py`](tools/spicetify.py) maps them onto the roles of Schemify's Modern preset ([`themes/template.records`](themes/template.records)):

- Panels and cards keep the scheme's own surfaces, text and accent.
- The canvas uses the scheme's background, its accent for wires, its text for labels, and a second scheme colour for symbols.
- The result is one row of [`themes/palettes.tsv`](themes/palettes.tsv).

Each scheme then has to pass Schemify's theme gate ([`tools/check_theme.py`](tools/check_theme.py), from Schemify's `schemify-theme` skill):
- WCAG contrast for canvas layers and chrome text.
- A visible grid that stays dimmer than the circuit.
- Net highlights that stay distinct under deuteranopia and protanopia.

When a colour misses a threshold, the generator moves it toward white or black until it passes, so its hue stays the theme's. When a surface makes the scheme's text unreadable, the surface moves back toward the background instead. When Modern's highlight set clashes with a background, a greedy search picks a new set. The gate's two-accent budget is reported but not enforced, because many of these themes are colourful by design.

The plugin embeds the template and the palette table (about 90 KB of wasm) and fills in the chosen scheme at run time.

### Regenerating

```sh
git clone https://github.com/spicetify/spicetify-themes /tmp/spicetify-themes   # revision used: see tools/spicetify.rev
python3 tools/spicetify.py /tmp/spicetify-themes                                 # rewrites themes/palettes.tsv
curl -fsSL -o ui.records https://raw.githubusercontent.com/OpenFAT/Schemify/main/ui/default-plugin/ui.records
python3 tools/gate.py ui.records                                                 # every scheme must pass
./build.sh                                                                       # rebuilds schemify_themes.wasm (Rust 1.95, wasm32)
```

To regenerate the screenshots, copy [`tools/shots.rs`](tools/shots.rs) into a Schemify checkout as `crates/view/app/tests/theme_shots.rs`, then make `Session::open_with` public in `tests/common/mod.rs`. Then run:

```sh
THEMES_DIR=$PWD cargo test -p schemify-app --test theme_shots
```

This loads the built plugin through the real editor, applies every scheme, checks that the canvas shows that scheme's background, and writes the PNGs. Downscale them into `screenshots/thumbs/` (640 px wide).

## Gallery

### Blossom

From spicetify's [Blossom](https://github.com/spicetify/spicetify-themes/tree/master/Blossom) by [Robatortas](https://github.com/Robatortas).

<table>
<tr><td align="center"><img src="screenshots/thumbs/blossom.dark.png" width="300" alt="Blossom dark"><br><b>dark</b><br><code>theme.blossom.dark</code></td></tr>
</table>

### BurntSienna

From spicetify's [BurntSienna](https://github.com/spicetify/spicetify-themes/tree/master/BurntSienna) by [pjaspinski](https://github.com/pjaspinski).

<table>
<tr><td align="center"><img src="screenshots/thumbs/burntsienna.base.png" width="300" alt="BurntSienna Base"><br><b>Base</b><br><code>theme.burntsienna.base</code></td></tr>
</table>

### Default

From spicetify's [Default](https://github.com/spicetify/spicetify-themes/tree/master/Default) by [Blacksuan19](https://github.com/Blacksuan19).

<table>
<tr><td align="center"><img src="screenshots/thumbs/default.ocean.png" width="300" alt="Default Ocean"><br><b>Ocean</b><br><code>theme.default.ocean</code></td></tr>
</table>

### Dreary

From spicetify's [Dreary](https://github.com/spicetify/spicetify-themes/tree/master/Dreary) by [CharlieS1103](https://github.com/CharlieS1103).

<table>
<tr><td align="center"><img src="screenshots/thumbs/dreary.psycho.png" width="300" alt="Dreary Psycho"><br><b>Psycho</b><br><code>theme.dreary.psycho</code></td><td align="center"><img src="screenshots/thumbs/dreary.deeper.png" width="300" alt="Dreary Deeper"><br><b>Deeper</b><br><code>theme.dreary.deeper</code></td><td align="center"><img src="screenshots/thumbs/dreary.bib.png" width="300" alt="Dreary BIB"><br><b>BIB</b><br><code>theme.dreary.bib</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/dreary.mono.png" width="300" alt="Dreary Mono"><br><b>Mono</b><br><code>theme.dreary.mono</code></td><td align="center"><img src="screenshots/thumbs/dreary.golden.png" width="300" alt="Dreary Golden"><br><b>Golden</b><br><code>theme.dreary.golden</code></td><td align="center"><img src="screenshots/thumbs/dreary.graytone_blue.png" width="300" alt="Dreary Graytone-Blue"><br><b>Graytone-Blue</b><br><code>theme.dreary.graytone_blue</code></td></tr>
</table>

### Dribbblish

From spicetify's [Dribbblish](https://github.com/spicetify/spicetify-themes/tree/master/Dribbblish) by [khanhas](https://github.com/khanhas), [harbassan](https://github.com/harbassan).

<table>
<tr><td align="center"><img src="screenshots/thumbs/dribbblish.base.png" width="300" alt="Dribbblish base"><br><b>base</b><br><code>theme.dribbblish.base</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.white.png" width="300" alt="Dribbblish white"><br><b>white</b><br><code>theme.dribbblish.white</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.dark.png" width="300" alt="Dribbblish dark"><br><b>dark</b><br><code>theme.dribbblish.dark</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/dribbblish.dracula.png" width="300" alt="Dribbblish dracula"><br><b>dracula</b><br><code>theme.dribbblish.dracula</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.nord_light.png" width="300" alt="Dribbblish nord-light"><br><b>nord-light</b><br><code>theme.dribbblish.nord_light</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.nord_dark.png" width="300" alt="Dribbblish nord-dark"><br><b>nord-dark</b><br><code>theme.dribbblish.nord_dark</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/dribbblish.purple.png" width="300" alt="Dribbblish purple"><br><b>purple</b><br><code>theme.dribbblish.purple</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.samurai.png" width="300" alt="Dribbblish samurai"><br><b>samurai</b><br><code>theme.dribbblish.samurai</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.beach_sunset.png" width="300" alt="Dribbblish beach-sunset"><br><b>beach-sunset</b><br><code>theme.dribbblish.beach_sunset</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/dribbblish.gruvbox.png" width="300" alt="Dribbblish gruvbox"><br><b>gruvbox</b><br><code>theme.dribbblish.gruvbox</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.gruvbox_material_dark.png" width="300" alt="Dribbblish gruvbox-material-dark"><br><b>gruvbox-material-dark</b><br><code>theme.dribbblish.gruvbox_material_dark</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.rosepine.png" width="300" alt="Dribbblish rosepine"><br><b>rosepine</b><br><code>theme.dribbblish.rosepine</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/dribbblish.lunar.png" width="300" alt="Dribbblish lunar"><br><b>lunar</b><br><code>theme.dribbblish.lunar</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.catppuccin_latte.png" width="300" alt="Dribbblish catppuccin-latte"><br><b>catppuccin-latte</b><br><code>theme.dribbblish.catppuccin_latte</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.catppuccin_frappe.png" width="300" alt="Dribbblish catppuccin-frappe"><br><b>catppuccin-frappe</b><br><code>theme.dribbblish.catppuccin_frappe</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/dribbblish.catppuccin_macchiato.png" width="300" alt="Dribbblish catppuccin-macchiato"><br><b>catppuccin-macchiato</b><br><code>theme.dribbblish.catppuccin_macchiato</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.catppuccin_mocha.png" width="300" alt="Dribbblish catppuccin-mocha"><br><b>catppuccin-mocha</b><br><code>theme.dribbblish.catppuccin_mocha</code></td><td align="center"><img src="screenshots/thumbs/dribbblish.tokyo_night.png" width="300" alt="Dribbblish tokyo-night"><br><b>tokyo-night</b><br><code>theme.dribbblish.tokyo_night</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/dribbblish.kanagawa.png" width="300" alt="Dribbblish kanagawa"><br><b>kanagawa</b><br><code>theme.dribbblish.kanagawa</code></td></tr>
</table>

### Flow

From spicetify's [Flow](https://github.com/spicetify/spicetify-themes/tree/master/Flow) by [Ian Liao](https://github.com/ian-Liaozy), [Victoria Zhang](https://github.com/Ruixi-Zhang), [Yu Sung Lee](https://github.com/yslDevelop), [Alex Casieri](https://github.com/alexcasieri30).

<table>
<tr><td align="center"><img src="screenshots/thumbs/flow.pink.png" width="300" alt="Flow Pink"><br><b>Pink</b><br><code>theme.flow.pink</code></td><td align="center"><img src="screenshots/thumbs/flow.green.png" width="300" alt="Flow Green"><br><b>Green</b><br><code>theme.flow.green</code></td><td align="center"><img src="screenshots/thumbs/flow.silver.png" width="300" alt="Flow Silver"><br><b>Silver</b><br><code>theme.flow.silver</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/flow.violet.png" width="300" alt="Flow Violet"><br><b>Violet</b><br><code>theme.flow.violet</code></td><td align="center"><img src="screenshots/thumbs/flow.ocean.png" width="300" alt="Flow Ocean"><br><b>Ocean</b><br><code>theme.flow.ocean</code></td></tr>
</table>

### Matte

From spicetify's [Matte](https://github.com/spicetify/spicetify-themes/tree/master/Matte) by [darkthemer](https://github.com/darkthemer).

<table>
<tr><td align="center"><img src="screenshots/thumbs/matte.matte.png" width="300" alt="Matte matte"><br><b>matte</b><br><code>theme.matte.matte</code></td><td align="center"><img src="screenshots/thumbs/matte.periwinkle.png" width="300" alt="Matte periwinkle"><br><b>periwinkle</b><br><code>theme.matte.periwinkle</code></td><td align="center"><img src="screenshots/thumbs/matte.periwinkle_dark.png" width="300" alt="Matte periwinkle-dark"><br><b>periwinkle-dark</b><br><code>theme.matte.periwinkle_dark</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/matte.porcelain.png" width="300" alt="Matte porcelain"><br><b>porcelain</b><br><code>theme.matte.porcelain</code></td><td align="center"><img src="screenshots/thumbs/matte.rose_pine_moon.png" width="300" alt="Matte rose-pine-moon"><br><b>rose-pine-moon</b><br><code>theme.matte.rose_pine_moon</code></td><td align="center"><img src="screenshots/thumbs/matte.gray_dark1.png" width="300" alt="Matte gray-dark1"><br><b>gray-dark1</b><br><code>theme.matte.gray_dark1</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/matte.gray_dark2.png" width="300" alt="Matte gray-dark2"><br><b>gray-dark2</b><br><code>theme.matte.gray_dark2</code></td><td align="center"><img src="screenshots/thumbs/matte.gray_dark3.png" width="300" alt="Matte gray-dark3"><br><b>gray-dark3</b><br><code>theme.matte.gray_dark3</code></td><td align="center"><img src="screenshots/thumbs/matte.gray.png" width="300" alt="Matte gray"><br><b>gray</b><br><code>theme.matte.gray</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/matte.gray_light.png" width="300" alt="Matte gray-light"><br><b>gray-light</b><br><code>theme.matte.gray_light</code></td></tr>
</table>

### Nightlight

From spicetify's [Nightlight](https://github.com/spicetify/spicetify-themes/tree/master/Nightlight).

<table>
<tr><td align="center"><img src="screenshots/thumbs/nightlight.nightlight_colors.png" width="300" alt="Nightlight Nightlight Colors"><br><b>Nightlight Colors</b><br><code>theme.nightlight.nightlight_colors</code></td></tr>
</table>

### Onepunch

From spicetify's [Onepunch](https://github.com/spicetify/spicetify-themes/tree/master/Onepunch) by [okarin001](https://github.com/okarin001).

<table>
<tr><td align="center"><img src="screenshots/thumbs/onepunch.dark.png" width="300" alt="Onepunch dark"><br><b>dark</b><br><code>theme.onepunch.dark</code></td><td align="center"><img src="screenshots/thumbs/onepunch.light.png" width="300" alt="Onepunch light"><br><b>light</b><br><code>theme.onepunch.light</code></td><td align="center"><img src="screenshots/thumbs/onepunch.legacy.png" width="300" alt="Onepunch legacy"><br><b>legacy</b><br><code>theme.onepunch.legacy</code></td></tr>
</table>

### SharkBlue

From spicetify's [SharkBlue](https://github.com/spicetify/spicetify-themes/tree/master/SharkBlue) by [Mr Biscuit](https://github.com/MrBiscuit921).

<table>
<tr><td align="center"><img src="screenshots/thumbs/sharkblue.base.png" width="300" alt="SharkBlue Base"><br><b>Base</b><br><code>theme.sharkblue.base</code></td></tr>
</table>

### Sleek

From spicetify's [Sleek](https://github.com/spicetify/spicetify-themes/tree/master/Sleek) by [harbassan](https://github.com/harbassan).

<table>
<tr><td align="center"><img src="screenshots/thumbs/sleek.wealthy.png" width="300" alt="Sleek Wealthy"><br><b>Wealthy</b><br><code>theme.sleek.wealthy</code></td><td align="center"><img src="screenshots/thumbs/sleek.cherry.png" width="300" alt="Sleek Cherry"><br><b>Cherry</b><br><code>theme.sleek.cherry</code></td><td align="center"><img src="screenshots/thumbs/sleek.coral.png" width="300" alt="Sleek Coral"><br><b>Coral</b><br><code>theme.sleek.coral</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/sleek.deep.png" width="300" alt="Sleek Deep"><br><b>Deep</b><br><code>theme.sleek.deep</code></td><td align="center"><img src="screenshots/thumbs/sleek.greener.png" width="300" alt="Sleek Greener"><br><b>Greener</b><br><code>theme.sleek.greener</code></td><td align="center"><img src="screenshots/thumbs/sleek.deeper.png" width="300" alt="Sleek Deeper"><br><b>Deeper</b><br><code>theme.sleek.deeper</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/sleek.psycho.png" width="300" alt="Sleek Psycho"><br><b>Psycho</b><br><code>theme.sleek.psycho</code></td><td align="center"><img src="screenshots/thumbs/sleek.ultrablack.png" width="300" alt="Sleek UltraBlack"><br><b>UltraBlack</b><br><code>theme.sleek.ultrablack</code></td><td align="center"><img src="screenshots/thumbs/sleek.nord.png" width="300" alt="Sleek Nord"><br><b>Nord</b><br><code>theme.sleek.nord</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/sleek.futura.png" width="300" alt="Sleek Futura"><br><b>Futura</b><br><code>theme.sleek.futura</code></td><td align="center"><img src="screenshots/thumbs/sleek.elementary.png" width="300" alt="Sleek Elementary"><br><b>Elementary</b><br><code>theme.sleek.elementary</code></td><td align="center"><img src="screenshots/thumbs/sleek.bladerunner.png" width="300" alt="Sleek BladeRunner"><br><b>BladeRunner</b><br><code>theme.sleek.bladerunner</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/sleek.dracula.png" width="300" alt="Sleek Dracula"><br><b>Dracula</b><br><code>theme.sleek.dracula</code></td><td align="center"><img src="screenshots/thumbs/sleek.vantablack.png" width="300" alt="Sleek VantaBlack"><br><b>VantaBlack</b><br><code>theme.sleek.vantablack</code></td><td align="center"><img src="screenshots/thumbs/sleek.rosepine.png" width="300" alt="Sleek RosePine"><br><b>RosePine</b><br><code>theme.sleek.rosepine</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/sleek.eldritch.png" width="300" alt="Sleek Eldritch"><br><b>Eldritch</b><br><code>theme.sleek.eldritch</code></td><td align="center"><img src="screenshots/thumbs/sleek.catppuccin.png" width="300" alt="Sleek Catppuccin"><br><b>Catppuccin</b><br><code>theme.sleek.catppuccin</code></td><td align="center"><img src="screenshots/thumbs/sleek.ayudark.png" width="300" alt="Sleek AyuDark"><br><b>AyuDark</b><br><code>theme.sleek.ayudark</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/sleek.tokyonight.png" width="300" alt="Sleek TokyoNight"><br><b>TokyoNight</b><br><code>theme.sleek.tokyonight</code></td></tr>
</table>

### StarryNight

From spicetify's [StarryNight](https://github.com/spicetify/spicetify-themes/tree/master/StarryNight) by [Brandon Chen](https://github.com/b-chen00), [Julissa Laignelet](https://github.com/laignelet16).

<table>
<tr><td align="center"><img src="screenshots/thumbs/starrynight.base.png" width="300" alt="StarryNight Base"><br><b>Base</b><br><code>theme.starrynight.base</code></td><td align="center"><img src="screenshots/thumbs/starrynight.cotton_candy.png" width="300" alt="StarryNight Cotton-candy"><br><b>Cotton-candy</b><br><code>theme.starrynight.cotton_candy</code></td><td align="center"><img src="screenshots/thumbs/starrynight.forest.png" width="300" alt="StarryNight Forest"><br><b>Forest</b><br><code>theme.starrynight.forest</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/starrynight.galaxy.png" width="300" alt="StarryNight Galaxy"><br><b>Galaxy</b><br><code>theme.starrynight.galaxy</code></td><td align="center"><img src="screenshots/thumbs/starrynight.orange.png" width="300" alt="StarryNight Orange"><br><b>Orange</b><br><code>theme.starrynight.orange</code></td><td align="center"><img src="screenshots/thumbs/starrynight.sky.png" width="300" alt="StarryNight Sky"><br><b>Sky</b><br><code>theme.starrynight.sky</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/starrynight.sunrise.png" width="300" alt="StarryNight Sunrise"><br><b>Sunrise</b><br><code>theme.starrynight.sunrise</code></td></tr>
</table>

### Turntable

From spicetify's [Turntable](https://github.com/spicetify/spicetify-themes/tree/master/Turntable) by [Grason Chan](https://github.com/grasonchan).

<table>
<tr><td align="center"><img src="screenshots/thumbs/turntable.turntable.png" width="300" alt="Turntable turntable"><br><b>turntable</b><br><code>theme.turntable.turntable</code></td></tr>
</table>

### Ziro

From spicetify's [Ziro](https://github.com/spicetify/spicetify-themes/tree/master/Ziro) by [schnensch0](https://github.com/schnensch0).

<table>
<tr><td align="center"><img src="screenshots/thumbs/ziro.blue_dark.png" width="300" alt="Ziro blue-dark"><br><b>blue-dark</b><br><code>theme.ziro.blue_dark</code></td><td align="center"><img src="screenshots/thumbs/ziro.blue_light.png" width="300" alt="Ziro blue-light"><br><b>blue-light</b><br><code>theme.ziro.blue_light</code></td><td align="center"><img src="screenshots/thumbs/ziro.gray_dark.png" width="300" alt="Ziro gray-dark"><br><b>gray-dark</b><br><code>theme.ziro.gray_dark</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/ziro.gray_light.png" width="300" alt="Ziro gray-light"><br><b>gray-light</b><br><code>theme.ziro.gray_light</code></td><td align="center"><img src="screenshots/thumbs/ziro.green_dark.png" width="300" alt="Ziro green-dark"><br><b>green-dark</b><br><code>theme.ziro.green_dark</code></td><td align="center"><img src="screenshots/thumbs/ziro.green_light.png" width="300" alt="Ziro green-light"><br><b>green-light</b><br><code>theme.ziro.green_light</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/ziro.orange_dark.png" width="300" alt="Ziro orange-dark"><br><b>orange-dark</b><br><code>theme.ziro.orange_dark</code></td><td align="center"><img src="screenshots/thumbs/ziro.orange_light.png" width="300" alt="Ziro orange-light"><br><b>orange-light</b><br><code>theme.ziro.orange_light</code></td><td align="center"><img src="screenshots/thumbs/ziro.purple_dark.png" width="300" alt="Ziro purple-dark"><br><b>purple-dark</b><br><code>theme.ziro.purple_dark</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/ziro.purple_light.png" width="300" alt="Ziro purple-light"><br><b>purple-light</b><br><code>theme.ziro.purple_light</code></td><td align="center"><img src="screenshots/thumbs/ziro.red_dark.png" width="300" alt="Ziro red-dark"><br><b>red-dark</b><br><code>theme.ziro.red_dark</code></td><td align="center"><img src="screenshots/thumbs/ziro.red_light.png" width="300" alt="Ziro red-light"><br><b>red-light</b><br><code>theme.ziro.red_light</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/ziro.rose_pine.png" width="300" alt="Ziro rose-pine"><br><b>rose-pine</b><br><code>theme.ziro.rose_pine</code></td><td align="center"><img src="screenshots/thumbs/ziro.rose_pine_moon.png" width="300" alt="Ziro rose-pine-moon"><br><b>rose-pine-moon</b><br><code>theme.ziro.rose_pine_moon</code></td><td align="center"><img src="screenshots/thumbs/ziro.rose_pine_dawn.png" width="300" alt="Ziro rose-pine-dawn"><br><b>rose-pine-dawn</b><br><code>theme.ziro.rose_pine_dawn</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/ziro.tokyo_night.png" width="300" alt="Ziro tokyo-night"><br><b>tokyo-night</b><br><code>theme.ziro.tokyo_night</code></td></tr>
</table>

### text

From spicetify's [text](https://github.com/spicetify/spicetify-themes/tree/master/text) by [darkthemer](https://github.com/darkthemer).

<table>
<tr><td align="center"><img src="screenshots/thumbs/text.spotify.png" width="300" alt="text Spotify"><br><b>Spotify</b><br><code>theme.text.spotify</code></td><td align="center"><img src="screenshots/thumbs/text.spicetify.png" width="300" alt="text Spicetify"><br><b>Spicetify</b><br><code>theme.text.spicetify</code></td><td align="center"><img src="screenshots/thumbs/text.catppuccinmocha.png" width="300" alt="text CatppuccinMocha"><br><b>CatppuccinMocha</b><br><code>theme.text.catppuccinmocha</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/text.catppuccinmacchiato.png" width="300" alt="text CatppuccinMacchiato"><br><b>CatppuccinMacchiato</b><br><code>theme.text.catppuccinmacchiato</code></td><td align="center"><img src="screenshots/thumbs/text.catppuccinlatte.png" width="300" alt="text CatppuccinLatte"><br><b>CatppuccinLatte</b><br><code>theme.text.catppuccinlatte</code></td><td align="center"><img src="screenshots/thumbs/text.dracula.png" width="300" alt="text Dracula"><br><b>Dracula</b><br><code>theme.text.dracula</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/text.gruvbox.png" width="300" alt="text Gruvbox"><br><b>Gruvbox</b><br><code>theme.text.gruvbox</code></td><td align="center"><img src="screenshots/thumbs/text.gruvboxhard.png" width="300" alt="text GruvboxHard"><br><b>GruvboxHard</b><br><code>theme.text.gruvboxhard</code></td><td align="center"><img src="screenshots/thumbs/text.kanagawa.png" width="300" alt="text Kanagawa"><br><b>Kanagawa</b><br><code>theme.text.kanagawa</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/text.nord.png" width="300" alt="text Nord"><br><b>Nord</b><br><code>theme.text.nord</code></td><td align="center"><img src="screenshots/thumbs/text.rigel.png" width="300" alt="text Rigel"><br><b>Rigel</b><br><code>theme.text.rigel</code></td><td align="center"><img src="screenshots/thumbs/text.rosepine.png" width="300" alt="text RosePine"><br><b>RosePine</b><br><code>theme.text.rosepine</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/text.rosepinemoon.png" width="300" alt="text RosePineMoon"><br><b>RosePineMoon</b><br><code>theme.text.rosepinemoon</code></td><td align="center"><img src="screenshots/thumbs/text.rosepinedawn.png" width="300" alt="text RosePineDawn"><br><b>RosePineDawn</b><br><code>theme.text.rosepinedawn</code></td><td align="center"><img src="screenshots/thumbs/text.solarized.png" width="300" alt="text Solarized"><br><b>Solarized</b><br><code>theme.text.solarized</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/text.tokyonight.png" width="300" alt="text TokyoNight"><br><b>TokyoNight</b><br><code>theme.text.tokyonight</code></td><td align="center"><img src="screenshots/thumbs/text.tokyonightstorm.png" width="300" alt="text TokyoNightStorm"><br><b>TokyoNightStorm</b><br><code>theme.text.tokyonightstorm</code></td><td align="center"><img src="screenshots/thumbs/text.forestgreen.png" width="300" alt="text ForestGreen"><br><b>ForestGreen</b><br><code>theme.text.forestgreen</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/text.everforestdarkhard.png" width="300" alt="text EverforestDarkHard"><br><b>EverforestDarkHard</b><br><code>theme.text.everforestdarkhard</code></td><td align="center"><img src="screenshots/thumbs/text.everforestdarkmedium.png" width="300" alt="text EverforestDarkMedium"><br><b>EverforestDarkMedium</b><br><code>theme.text.everforestdarkmedium</code></td><td align="center"><img src="screenshots/thumbs/text.everforestdarksoft.png" width="300" alt="text EverforestDarkSoft"><br><b>EverforestDarkSoft</b><br><code>theme.text.everforestdarksoft</code></td></tr>
<tr><td align="center"><img src="screenshots/thumbs/text.flexokilight.png" width="300" alt="text FlexokiLight"><br><b>FlexokiLight</b><br><code>theme.text.flexokilight</code></td><td align="center"><img src="screenshots/thumbs/text.flexokidark.png" width="300" alt="text FlexokiDark"><br><b>FlexokiDark</b><br><code>theme.text.flexokidark</code></td><td align="center"><img src="screenshots/thumbs/text.bloodmoon.png" width="300" alt="text BloodMoon"><br><b>BloodMoon</b><br><code>theme.text.bloodmoon</code></td></tr>
</table>

## License

MIT (see [LICENSE](LICENSE)). The colour schemes come from [spicetify-themes](https://github.com/spicetify/spicetify-themes) (MIT, © morpheusthewhite and contributors); each theme's authors are credited above.
