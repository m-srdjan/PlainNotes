
# [PlainNotes](https://github.com/m-srdjan/PlainNotes)
Simple and pleasant authoring and note taking for SublimeText.

> **This is a maintained fork** of [aziz/PlainNotes](https://github.com/aziz/PlainNotes),
> which has had no changes since 2017. It targets Sublime Text 4. See
> [Changes in this fork](#changes-in-this-fork) and [Installing this fork](#installing-this-fork).

With PlainNotes you can:
 - Organize notes and thoughts
 - Maintain todo-lists
 - Write documents
 - and probably more

PlainNotes stores and organizes all your notes in a folder and make them
accessible with a single shortcut or mouse click. It also provides you with an
enhanced version of Markdown markup and some good looking color schemes for
note taking.
It's been designed with these ground rules in mind:
 - Plain text is the holy grail
 - Plain text shouldn't be that plain
 - Simple and Sexy is Sublime

<p align="center">
<img src="http://cl.ly/image/21143i2m3e0n/ss2.png" width="727" height="416">
</p>

**Note:** This fork is developed and tested on Sublime Text 4 only. The
syntax definitions rely on `embed`/`escape` (build 3153+), so Sublime Text 2
is no longer supported.

## Changes in this fork

- **Fenced code blocks no longer break highlighting.** A block tagged `css`,
  `js`, `python` and so on used to swallow its closing fence, so everything
  after it was highlighted as code. The closing fence now always ends the
  block, whatever state the embedded language is in.
- **Inline and block HTML are contained.** An unclosed tag (`a <b and c`),
  comment or `<style>` used to turn the rest of the note into HTML or CSS.
  Only a complete tag on a line now counts as HTML, and HTML blocks end at
  their closing tag or at a blank line (CommonMark).
- **More fenced-block languages**, case-insensitive, with text allowed after
  the language name (```` ```js title="x.js" ````). See
  [Fenced code blocks](#fenced-code-blocks).
- **Legacy `.tmLanguage` copies removed**; the `.sublime-syntax` files are
  the only syntax definitions.
- **Syntax tests** in `Tests/syntax_test_*.note`.

Full details are in [CHANGELOG.md](CHANGELOG.md).

## Installing this fork

The fork is not on Package Control. Install it by cloning into your
`Packages` folder (`Preferences -> Browse Packages…`):

1. If you have the Package Control version, remove it first
   (`Package Control: Remove Package` → `PlainNotes`).
2. Clone the fork into `Packages/PlainNotes`:

   ```sh
   git clone https://github.com/m-srdjan/PlainNotes.git PlainNotes
   ```

Package Control will not replace a git checkout with its own release; when it
upgrades packages it runs `git pull` on the checkout instead, so the fork
stays up to date. To stop that, add `"PlainNotes"` to `ignore_vcs_packages`
in the Package Control settings and update with `git pull` yourself.

If you want the working copy somewhere else, keep the real folder in
`Packages` and link to it from elsewhere, not the other way round. Sublime's
file watcher does not follow links into `Packages`, so a package behind a
junction or symlink will not reload when you edit it.

## Organizing notes

Most of PlainNotes commands are accessible from the SublimeText main menu. You
should have a menu item called `Notes` right after `Help`. Although, there are
faster and easier ways of running those commnads that are mentioned below.

#### Starting a new note (`super+F4`)
- **Command palette**: Open command palette and search for `Notes: new`
  command (typing `nn` will probably find it for you).
  - To save note in a subfolder of the root directory use `/`:
    `"subfolder name"/"note name"`.

- **Shortcut**: By default pressing <kbd>super+F4</kbd> will create a new
  note. For customizing the shortcut see [Keyboard Shortcuts]() section.

#### Opening an existing note (`F4`)
- **Command palette**: Open command palette and search for `Notes: List…`
  command (typing `nl` will probably find it for you), the command will show
  the *Latest Notes quick panel* from which you can select or search for your
  file.
  The *Latest Notes quick panel* is sorting files based on their last-edit
  time, so the note that you have been working on recently should be on top of
  the list.

- **Shortcut**: By default pressing <kbd>F4</kbd> will open the
  *Latest Notes quick panel*. For customizing the shortcut see
  [Keyboard Shortcuts]() section.

#### Jotter (`F1`)
Jotter will let you jot down your thoughts and ideas quickly without
disturbing your work-flow. It opens a *Note Panel* at the bottom of the editor
which is ready to take your note. When you press <kbd>ESC</kbd> it
automatically closes the panel and saves your note with a time stamp in your
*Inbox*.

It can be accessed by pressing <kbd>F1</kbd> (that can be customized in your
Key-bindings if it conflicts with your other key-bindings) or through
`Notes: Jotter` in command palette.
The default color scheme of the jotter panel can be customized in user
settings (`Preferences -> Package Settings -> PlainNotes -> Settings`):

```json
{ "jotter_color_scheme": "Packages/PlainNotes/Color Schemes/Sticky-Yellow.tmTheme" }
```

#### Inbox
Inbox is where all your quick notes from *Jotter* live. You can view inbox
through `Notes: Inbox` in command palette or via the Notes main menu.
The date and time format of the note headers in inbox can be customized in user
settings (`Preferences -> Package Settings -> PlainNotes -> Settings`):

```json
{
    "jotter_date_format": "%d %b %Y",
    "jotter_time_format": "%I:%M %p"
}
```

#### Notes Index Card (`ctrl+F4`)
Pressing <kbd>ctrl+F4</kbd> or selecting `Notes: Index` from the command
palette will give you the *Notes Index Card* with the list of all notes sorted
alphabetically, grouped under their folders (`▣`). Hidden folders (names
starting with `.`) are left out.
Pressing <kbd>Enter</kbd> on any note will open it in a new tab. Pressing
<kbd>Enter</kbd> on a folder asks for a title and creates a new note in that
folder.
The color scheme of the index can be customized in user settings:

```json
{ "index_color_scheme": "Packages/PlainNotes/Color Schemes/Sticky-Yellow.tmTheme" }
```

#### Change note color
Open command palette and search for `Note: Change Color…`. it will give you a
list of 10 different colors that is shown in the above image. Pressing up and
down will give you a preview.
Color of the note is remembered by PlainNotes and whenever you open that file,
PlainNotes will set the color-scheme automatically.

#### Delete note
Open a note and then open command palette and search for `Note: Delete`.

#### Rename note
Open a note and then open command palette and search for `Note: Rename`.

#### Change note file extension
You can change the note file extension in settings. To do so, go to
`Preferences -> Package Settings -> PlainNotes -> Settings` and modify
`"note_save_extension":`. The default note type is `.note` which has the
possibility of setting different note colors and some special markup.
Alternatively you can use any note extension you want such as markdown `.md`.

#### Add yaml front matter to notes
Go to `Preferences -> Package Settings -> PlainNotes -> Settings` and
modify `"enable_yaml"`

By default, the following yaml items are added:
```yaml
title:
date:
tags:
```

To add more yaml items you can add them to the settings by modifying `note_yaml:`:

```json
{ "note_yaml" : ["categories"] }
```

#### Other features
- **Open URLs**: place cursor on the link then press `enter` to open a url in
  the browser.
- **Preview images inline**: place cursor on a markdown image with inline image url and press `enter` to a preview popup of that image. You should have ST 3070 or newer for this feature to work.

#### Per-project notes

To have a different notes directory for a project, add the following in your
`.sublime-project` file:

```json
"settings": {
    "PlainNotes": {
        "root": "path/to/notes/dir"
    }
}
```

## Authoring notes
PlainNotes provides an enhanced version of Markdown. It means that you can
write your notes in plain markdown without learning anything new. In addition,
it gives you some extra markups to improve the look and feel of your
documents, since markdown sometime feels too simple to format a real document.

If you are new to markdown here is a cheat-sheet:

|    Markup   |            Markdown Syntax            |
|-------------|---------------------------------------|
| Italic      | `_italic_` or `*italic*`              |
| Bold        | `__bold__` or `**bold**`              |
| Images      | `![Image Title](http://url_to.image)` |
| Links       | `[Link Text](http://link.url)`        |
| Inline Code | `` `code` ``                          |
| Quotes      | `> Here is a quote block`             |
| Separators  | `----` or `*****`                     |
| Heading 1   | `# Heading 1`                         |
| Heading 2   | `## Heading 2`                        |
| Heading 3   | `### Heading 3`                       |
| Heading 4   | `#### Heading 4`                      |

### Extra Markup

#### Fenced code blocks
Fence code with ```` ``` ```` or `~~~` and name the language to get it
highlighted. The name is case-insensitive and may be followed by other text.

````
```python
def hello():
    return "world"
```
````

| Language   | Tags                                          |
|------------|-----------------------------------------------|
| Batch      | `bat` `batch` `cmd` `dosbatch`                |
| C / C++    | `c` `h` / `c++` `cpp` `cxx` `cc` `hpp`        |
| C#         | `cs` `csharp` `c#`                            |
| Clojure    | `clojure` `clj` `cljs`                        |
| CoffeeScript | `coffee` `coffeescript`                     |
| CSS / Less / Sass / SCSS | `css` / `less` / `sass` / `scss` |
| Diff       | `diff` `patch`                                |
| Erlang     | `erlang` `erl`                                |
| Go         | `go` `golang`                                 |
| Haskell    | `haskell` `hs`                                |
| HTML / XML | `html` `htm` `xhtml` / `xml` `svg` `xsl` `xslt` `plist` |
| Java       | `java`                                        |
| JavaScript | `js` `javascript` `mjs` `cjs` `node`          |
| JSON       | `json` `jsonc` `json5`                        |
| JSX / TSX  | `jsx` / `tsx`                                 |
| LaTeX / TeX | `latex` / `tex`                              |
| Lisp       | `lisp` `elisp`                                |
| Lua        | `lua`                                         |
| Makefile   | `makefile` `make` `mk`                        |
| Markdown   | `markdown` `md`                               |
| MATLAB     | `matlab`                                      |
| Objective-C | `objective-c` `objc`                         |
| Perl       | `perl` `pl`                                   |
| PHP        | `php`                                         |
| PowerShell | `powershell` `pwsh` `ps1` `posh`              |
| Python     | `python` `py` `py3`                           |
| R          | `r`                                           |
| Regex      | `regexp` `regex`                              |
| Ruby       | `ruby` `rb`                                   |
| Rust       | `rust` `rs`                                   |
| Scala      | `scala`                                       |
| Shell      | `sh` `shell` `bash` `console` `shell-script` / `zsh` |
| SQL        | `sql` `mysql` `psql` `postgres` `postgresql`  |
| TOML       | `toml`                                        |
| TypeScript | `ts` `typescript`                             |
| YAML       | `yaml` `yml`                                  |

CoffeeScript, Less, Sass/SCSS and PowerShell need their syntax packages
installed; the rest ship with Sublime Text. Blocks with any other tag, or none,
are shown as plain code.

#### Admonitions
When writing a note, you might need to distinguish a block or section by
giving it a special title and box. These sections might appear several times
in your document. Some examples would be *Note*, *Tip* or *Caution* blocks in
an article.

Here is how to create an admonition block

    !!! ADMONITION_TYPE "Optional title in quotes"
        Any number of other indented markdown elements.

<img width="640" src="https://cloud.githubusercontent.com/assets/3202/10559318/3d5e5420-74ee-11e5-89b9-0eca42750aca.png" >

By default admonitions block have a purplish background color (that might be
different based on the color scheme), but giving it a specific type from table
below can change the color. Predefined admonition types are listed in table
below and are shown in image above. Note that admonition types can be lower-
case, upper-case or title-case.

| Predefined Admonition Type | Block Color |
|----------------------------|-------------|
| `hint` or `tip`            | bluish      |
| `warning` or `caution`     | yellowish   |
| `danger` or `error`        | reddish     |
| `attention`                | greenish    |

Admonition blocks can have any PlainNotes enhanced markdown inside them and
they customize the look and feel so that everything looks sublime.

<img align="center" width="380" src="https://cloud.githubusercontent.com/assets/3202/10559414/c9a61ff6-74f0-11e5-8209-1c881ebd8506.png" >

## Development

- `Note-fenced.sublime-syntax` is generated. To add or change a fenced-block
  language, edit the `LANGS` table in `scripts/gen_fenced.py` and run
  `python scripts/gen_fenced.py` from the package root.
- Run the syntax tests with `Tools -> Build With… -> Syntax Tests` while a
  `Tests/syntax_test_*.note` file is open.

## License

Copyright 2014-2015 [Allen Bargi](https://twitter.com/aziz).
Licensed under the MIT License

