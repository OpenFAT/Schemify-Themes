//! Scratch harness (not for Schemify's repo): renders every Schemify-Themes scheme through the
//! real plugin. THEMES_DIR is the plugin checkout; PNGs land in $THEMES_DIR/screenshots/full.
mod common;
use common::Session;

fn slug(s: &str) -> String {
    s.chars().map(|c| if c.is_ascii_alphanumeric() { c.to_ascii_lowercase() } else { '_' }).collect()
}

#[test]
fn theme_shots() {
    let themes = std::path::PathBuf::from(std::env::var("THEMES_DIR").expect("THEMES_DIR"));
    let dir = common::fixture("inv", "theme-shots");
    let init = dir.join("init.lua");
    std::fs::write(
        &init,
        format!(
            "schemify.opt.simulator = \"espice\"\nschemify.pack.add {{ {{ path = [==[{}]==], name = 'schemify-themes' }} }}\n",
            themes.display()
        ),
    )
    .unwrap();
    let mut s = Session::open_with(dir, "top.shcomp", true, schemify_config::Startup::File(init));
    let out = themes.join("screenshots/full");
    let tsv = std::fs::read_to_string(themes.join("themes/palettes.tsv")).unwrap();
    let mut lines = tsv.lines();
    let head: Vec<&str> = lines.next().unwrap().split('\t').collect();
    let bg = head.iter().position(|h| *h == "c_bg").unwrap();
    for line in lines {
        let f: Vec<&str> = line.split('\t').collect();
        let id = format!("{}.{}", slug(f[0]), slug(f[1]));
        s.run(&format!("theme.{id}"), "");
        let px = s.render();
        let c = px.sample(1100, 200);
        let want = u32::from_str_radix(f[bg], 16).unwrap();
        assert_eq!(
            (c.r as u32) << 16 | (c.g as u32) << 8 | c.b as u32,
            want,
            "{id}: the canvas shows the scheme's background (status: {})",
            s.status()
        );
        common::save_png(&px, &out.join(format!("{id}.png")));
    }
    // The menu, open on one theme family, for the README.
    s.run("theme.sleek.nord", "");
    s.click_node("menu.view");
    s.click_node("menu.view.themes");
    s.click_node("themes.sleek");
    common::save_png(&s.render(), &out.join("_menu.png"));
}

#[test]
fn init_lua_applies_a_theme_at_startup() {
    let themes = std::path::PathBuf::from(std::env::var("THEMES_DIR").expect("THEMES_DIR"));
    let dir = common::fixture("inv", "theme-init");
    let init = dir.join("init.lua");
    std::fs::write(
        &init,
        format!(
            "schemify.pack.add {{ {{ path = [==[{}]==], name = 'schemify-themes', lazy = {{ cmd = 'theme.sleek.nord' }} }} }}\nschemify.cmd('theme.sleek.nord')\n",
            themes.display()
        ),
    )
    .unwrap();
    let mut s = Session::open_with(dir, "top.shcomp", true, schemify_config::Startup::File(init));
    s.frame(Default::default());
    let c = s.render().sample(1100, 200);
    println!("canvas after init.lua: {:02x}{:02x}{:02x} status={}", c.r, c.g, c.b, s.status());
}
