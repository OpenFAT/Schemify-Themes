//! Schemify-Themes: spicetify's theme catalogue as Schemify presets. View → Themes lists every
//! theme and its colour schemes; picking one re-contributes the UI set with that scheme's styles
//! (last contribution wins, D8). `theme.off` returns to the editor's own look.
//!
//! A scheme is one row of `themes/palettes.tsv`; its colours fill the `@token` slots of
//! `themes/template.records` (tools/spicetify.py writes both, tools/gate.py checks every row).

const TEMPLATE: &str = include_str!("../themes/template.records");
const PALETTES: &str = include_str!("../themes/palettes.tsv");

/// One palette row: theme, scheme, then one colour per header token.
pub struct Scheme<'a> {
    pub theme: &'a str,
    pub scheme: &'a str,
    pub colours: Vec<&'a str>,
}

/// The token names (palette header after theme, scheme, authors) and every scheme row.
pub fn schemes() -> (Vec<&'static str>, Vec<Scheme<'static>>) {
    let mut lines = PALETTES.lines();
    let head: Vec<&str> = lines
        .next()
        .expect("palette header")
        .split('\t')
        .skip(3)
        .collect();
    let rows = lines
        .map(|l| {
            let mut f = l.split('\t');
            let (theme, scheme) = (f.next().unwrap(), f.next().unwrap());
            let colours: Vec<&str> = f.skip(1).collect();
            assert_eq!(
                colours.len(),
                head.len(),
                "{theme}/{scheme}: one colour per token"
            );
            Scheme {
                theme,
                scheme,
                colours,
            }
        })
        .collect();
    (head, rows)
}

/// `Sleek`, `Nightlight Colors` → `sleek.nightlight_colors`: the id half of command and node names.
pub fn slug(theme: &str, scheme: &str) -> String {
    let clean = |s: &str| -> String {
        s.chars()
            .map(|c| {
                if c.is_ascii_alphanumeric() {
                    c.to_ascii_lowercase()
                } else {
                    '_'
                }
            })
            .collect()
    };
    format!("{}.{}", clean(theme), clean(scheme))
}

/// The template with every `@token` replaced by the scheme's colour.
pub fn expand(head: &[&str], s: &Scheme) -> String {
    let mut out = String::with_capacity(TEMPLATE.len());
    let mut rest = TEMPLATE;
    while let Some(at) = rest.find('@') {
        out.push_str(&rest[..at]);
        let tail = &rest[at + 1..];
        let end = tail
            .find(|c: char| !(c.is_ascii_alphanumeric() || c == '_'))
            .unwrap_or(tail.len());
        let i = head
            .iter()
            .position(|h| *h == &tail[..end])
            .expect("template token in palette header");
        out.push_str(s.colours[i]);
        rest = &tail[end..];
    }
    out.push_str(rest);
    out
}

/// The View → Themes menu, with the applied scheme checked.
fn menu(rows: &[Scheme], current: Option<usize>) -> String {
    let mut m = String::from(
        "node menu.view.themes menu\n  parent menu.view\n  label Themes\n\
         node themes.off item\n  parent menu.view.themes\n  label \"Schemify default\"\n  command theme.off\n",
    );
    let mut last = "";
    for (i, s) in rows.iter().enumerate() {
        let id = slug(s.theme, s.scheme);
        let family = id.split('.').next().unwrap();
        if s.theme != last {
            m += &format!(
                "node themes.{family} menu\n  parent menu.view.themes\n  label \"{}\"\n",
                s.theme
            );
            last = s.theme;
        }
        let on = u8::from(current == Some(i));
        m += &format!(
            "node themes.{id} item\n  parent themes.{family}\n  label \"{}\"\n  command theme.{id}\n  checked {on}\n",
            s.scheme
        );
    }
    m
}

pub fn commands(rows: &[Scheme]) -> String {
    let mut c = String::from("command theme.off \"Theme: Schemify default\"\n");
    for s in rows {
        c += &format!(
            "command theme.{} \"Theme: {} / {}\"\n",
            slug(s.theme, s.scheme),
            s.theme,
            s.scheme
        );
    }
    c
}

/// The whole UI set for `current`: the menu, then the scheme's styles.
pub fn ui(current: Option<usize>) -> String {
    let (head, rows) = schemes();
    let mut u = menu(&rows, current);
    if let Some(i) = current {
        u += &expand(&head, &rows[i]);
    }
    u
}

/// The wasm guest: the host's events in, UI and command contributions out.
#[cfg(target_arch = "wasm32")]
mod glue {
    use super::{commands, schemes, slug, ui};
    use schemify_abi::guest::{self, Host};
    use schemify_abi::{Event, Out};
    use std::cell::Cell;

    guest::export!(on_event);

    thread_local! {
        /// The applied scheme, an index into [`schemes`]. Not persisted: `init.lua` re-applies it
        /// on `load` (README).
        static CURRENT: Cell<Option<usize>> = const { Cell::new(None) };
    }

    fn on_event(ev: Event<'_>, _host: &Host, out: &mut Out) {
        match ev {
            Event::Load => {
                let (_, rows) = schemes();
                out.contribute_ui(&ui(CURRENT.get()));
                out.contribute_commands(&commands(&rows));
            }
            Event::Command { name, .. } if name.starts_with("theme.") => {
                let (_, rows) = schemes();
                let id = &name["theme.".len()..];
                let pick = rows.iter().position(|s| slug(s.theme, s.scheme) == id);
                if id != "off" && pick.is_none() {
                    return;
                }
                CURRENT.set(pick);
                // Immediate mode: re-declare the whole set; the host replaces the previous one.
                out.contribute_ui(&ui(pick));
            }
            _ => {}
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_scheme_expands_and_has_a_unique_command() {
        let (head, rows) = schemes();
        assert!(rows.len() >= 100, "the spicetify catalogue");
        let mut ids: Vec<String> = rows.iter().map(|s| slug(s.theme, s.scheme)).collect();
        for s in &rows {
            let text = expand(&head, s);
            assert!(!text.contains('@'), "{}/{}: token left", s.theme, s.scheme);
        }
        ids.sort();
        ids.dedup();
        assert_eq!(ids.len(), rows.len(), "command ids collide");
        assert!(ui(Some(0)).contains("checked 1"));
    }
}
