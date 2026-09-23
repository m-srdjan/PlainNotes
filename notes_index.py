# -*- coding: utf-8 -*-

import sublime, sublime_plugin
import os, fnmatch, re

TAB_SIZE = 2
COL_WIDTH = 30


def settings():
    return sublime.load_settings('Notes.sublime-settings')


def get_root():
    project_settings = sublime.active_window().active_view().settings().get('PlainNotes')
    if project_settings:
        return os.path.normpath(os.path.expanduser(project_settings.get('root',settings().get("root"))))
    else:
        return os.path.normpath(os.path.expanduser(settings().get("root")))

def brain_dir():
    # jotter_dir is the old name of data_dir, still honored in user settings
    brain_settings = settings().get("jotter_dir") or settings().get("data_dir")
    if brain_settings:
        return brain_settings
    else:
        return ".brain"


class NotesBufferCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.new_file()
        view.set_scratch(True)
        view.set_name(u"✎ Notes Index")
        view.set_syntax_file('Packages/PlainNotes/Notes Index.sublime-syntax')
        view.settings().set('color_scheme', settings().get('index_color_scheme', 'Packages/PlainNotes/Color Schemes/Notes-Index.hidden-tmTheme'))
        self.window.focus_view(view)
        view.run_command('notes_buffer_refresh')


class NotesBufferRefreshCommand(sublime_plugin.TextCommand):

    def run(self, edit, select_path=None):
        v = self.view
        row = v.rowcol(v.sel()[0].a)[0] if len(v.sel()) else 0
        v.set_read_only(False)
        v.erase(edit, sublime.Region(0, self.view.size()))
        root = get_root()
        lines = self.list_files(root)

        v.settings().set('notes_buffer_files', lines)

        v.insert(edit, 0, u"\n".join([f[0] for f in lines]))
        v.set_read_only(True)

        # put the cursor on the given item, or keep it on the same line
        if select_path:
            paths = [os.path.normcase(f[1]) for f in lines]
            target = os.path.normcase(os.path.normpath(select_path))
            if target in paths:
                row = paths.index(target)
        row = min(row, max(len(lines) - 1, 0))
        point = v.text_point(row, 0)
        v.sel().clear()
        v.sel().add(sublime.Region(point))
        v.show(point)

    def list_files(self, path):
        lines = []
        shown_ext = re.escape("." + settings().get("note_save_extension")) + "$"
        for root, dirs, files in os.walk(path, topdown=True):
            # skip hidden folders and the data folder, and list folders in order
            dirs[:] = sorted((d for d in dirs if not d.startswith(".") and d != brain_dir()), key=lambda d: d.lower())
            relpath = os.path.relpath(root, path)
            level = 0 if relpath == "." else relpath.count(os.sep) + 1
            if level:
                indent = ' ' * TAB_SIZE * (level - 1)
                line_str = u'{0}▣ {1}'.format(indent, os.path.basename(root))
                lines.append((line_str, os.path.normpath(root)))
            subindent = ' ' * TAB_SIZE * level
            for f in sorted(files, key=lambda f: f.lower()):
                for ext in settings().get("note_file_extensions"):  # display only files with given extension
                    if fnmatch.fnmatch(f, "*." + ext):
                        line_str = u'{0}≡ {1}'.format(subindent, re.sub(shown_ext, '', f))
                        line_path = os.path.normpath(os.path.join(root, f))
                        lines.append((line_str, line_path))
                        break
        return lines


class NotesBufferOpenCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        v = self.view
        for sel in v.sel():
            file_index = v.rowcol(sel.a)[0]
            files = v.settings().get('notes_buffer_files')
            file_path = files[file_index][1]
            if os.path.isdir(file_path):
                sublime.run_command("notes_new", {"directory": file_path})
            else:
                sublime.run_command("notes_open", {"file_path": file_path})


class NotesBufferMoveCommand(sublime_plugin.TextCommand):
    """Move or rename the note or folder under the cursor, or under a right-click."""

    def run(self, edit, event=None):
        if event:
            point = self.view.window_to_text((event["x"], event["y"]))
            self.view.sel().clear()
            self.view.sel().add(sublime.Region(point))
        files = self.view.settings().get('notes_buffer_files')
        if not files:
            return
        row = self.view.rowcol(self.view.sel()[0].a)[0]
        if row < len(files):
            sublime.run_command("notes_move", {"path": files[row][1]})

    def is_visible(self, event=None):
        return self.view.settings().get('notes_buffer_files') is not None

    def want_event(self):
        return True
