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
    brain_settings = settings().get("jotter_dir")
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

    def run(self, edit):
        v = self.view
        v.set_read_only(False)
        v.erase(edit, sublime.Region(0, self.view.size()))
        root = get_root()
        lines = self.list_files(root)

        v.settings().set('notes_buffer_files', lines)

        v.insert(edit, 0, u"\n".join([f[0] for f in lines]))
        v.set_read_only(True)

    def list_files(self, path):
        lines = []
        for root, dirs, files in os.walk(path, topdown=True):
            # skip hidden folders and the jotter folder, and list folders in order
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d != brain_dir())
            relpath = os.path.relpath(root, path)
            level = 0 if relpath == "." else relpath.count(os.sep) + 1
            if level:
                indent = ' ' * TAB_SIZE * (level - 1)
                line_str = u'{0}▣ {1}'.format(indent, os.path.basename(root))
                lines.append((line_str, root))
            subindent = ' ' * TAB_SIZE * level
            for f in sorted(files):
                for ext in settings().get("note_file_extensions"):  # display only files with given extension
                    if fnmatch.fnmatch(f, "*." + ext):
                        line_str = u'{0}≡ {1}'.format(subindent, re.sub(r'\.note$', '', f))
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
