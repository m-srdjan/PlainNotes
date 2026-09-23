# Changelog

Changes in the [m-srdjan/PlainNotes](https://github.com/m-srdjan/PlainNotes) fork.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
The fork starts from upstream [aziz/PlainNotes](https://github.com/aziz/PlainNotes)
`0.3.0` (2017-07-22); earlier history is in the upstream repository.

## [Unreleased]

### Added

- `index_color_scheme` setting for the color scheme of the Notes Index.
- `Preferences: PlainNotes Settings` and `Preferences: PlainNotes Key Bindings`
  in the command palette.
- Pressing Enter on a folder in the Notes Index creates a new note in that
  folder. It used to open an empty tab.
- Open Notes Index tabs refresh when a new note is created.

### Changed

- `Preferences -> Package Settings -> PlainNotes -> Settings` and `Key Bindings`
  open the defaults and your user file side by side in one window, replacing
  the separate Default and User menu items.
- The Notes Index lists folders top-down and alphabetically, each folder before
  its subfolders, and labels a folder with its own name instead of its full path.
- The Notes Index and the notes list skip hidden folders (names starting with
  `.`).
- `Notes: New…` accepts nested folders in the title (`work/2026/plan`); it used
  to keep only the first folder.

### Removed

- The Archive and Unarchive commands and the `archive_dir` setting. Use folders
  instead. An existing `.archive` folder is left on disk untouched.

## [0.4.0] - 2026-09-23

First release of the fork.

### Fixed

- Fenced code blocks tagged with a language (`css`, `js`, `python`, …) no longer
  swallow their closing fence and highlight the rest of the note as code.
  Languages are embedded with `embed`/`escape` instead of `include`, so the
  closing fence always ends the block.
- The `js` fence could close in the wrong place: its closing pattern was missing
  the `^` anchor.
- An unclosed inline tag (`a <b and c`), HTML comment, `<script>` or `<style>` no
  longer turns everything after it into HTML or CSS. Only a complete tag on a
  line counts as HTML, and each tag's highlighting ends at its `>` or at end of
  line. Text like `x<y` and `a <- b` stays plain text.
- HTML blocks end at their closing tag or at a blank line (CommonMark type 6).
  `<pre>`, `<script>`, `<style>` and `<textarea>` blocks end only at their
  closing tag, so blank lines inside them are fine.

### Added

- Fenced-block languages: TypeScript, TSX, JSX, JSON (was treated as
  JavaScript), TOML, Rust, Lua, C#, Batch, PowerShell, Zsh, Makefile, Markdown and
  Clojure, plus more aliases for existing languages (`py`, `yml`, `rb`, `sh`, …).
  See the table in the README.
- Language tags are case-insensitive (`JS` works).
- Text after the language name is allowed (```` ```js title="x.js" ````).
- `scripts/gen_fenced.py`, which generates `Note-fenced.sublime-syntax`.
- Syntax tests: `Tests/syntax_test_fenced.note` and `Tests/syntax_test_html.note`.
- README sections on the fork, installing it, fenced code blocks and development.
- This changelog.

### Changed

- Jotter and the Notes Index use the `.sublime-syntax` definitions.
- `.gitignore` ignores Color Highlight's `*.chback` backups.
- Sublime Text 4 is the target; Sublime Text 2 is no longer supported.

### Removed

- The legacy `Note.tmLanguage`, `Note-fenced.tmLanguage` and
  `Notes Index.hidden-tmLanguage` duplicates.

### Known limitations

- A multi-line HTML comment inside a paragraph is only highlighted as a comment
  on its first line.
- Inline `<script>`/`<style>` inside a paragraph (as opposed to an HTML block)
  get no JavaScript/CSS highlighting after the tag.

[Unreleased]: https://github.com/m-srdjan/PlainNotes/compare/0.4.0...master
[0.4.0]: https://github.com/m-srdjan/PlainNotes/compare/6a2d343...0.4.0
