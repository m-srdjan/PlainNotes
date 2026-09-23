# -*- coding: utf-8 -*-

import sublime, sublime_plugin
import os, fnmatch, re, time
import copy
import json

from .lib import helpers

ST3 = int(sublime.version()) >= 3000

if not ST3:
    from codecs import open


def settings():
    return sublime.load_settings('Notes.sublime-settings')


def get_root():
    project_settings = sublime.active_window().active_view().settings().get('PlainNotes')
    if project_settings:
        return os.path.normpath(os.path.expanduser(project_settings.get('root', settings().get("root"))))
    else:
        return os.path.normpath(os.path.expanduser(settings().get("root")))


def file_id(path):
    return os.path.relpath(path, root)

def brain_dir():
    # jotter_dir is the old name of data_dir, still honored in user settings
    brain_settings = settings().get("jotter_dir") or settings().get("data_dir")
    if brain_settings:
        return brain_settings
    else:
        return ".brain"


def find_notes(self, root, exclude):
    note_files = []
    for path, subdirs, files in os.walk(root, topdown=True):
        # skip hidden folders and excluded ones
        subdirs[:] = [d for d in subdirs if not d.startswith(".") and d not in exclude]
        relpath = os.path.relpath(path, root)
        for name in files:
            for ext in settings().get("note_file_extensions"):
                if (not relpath.startswith(brain_dir())) and fnmatch.fnmatch(name, "*." + ext):
                    title = re.sub('\.' + ext + '$', '', name)
                    tag = path.replace(root, '').replace(os.path.sep, '')
                    if not tag == '':
                        tag = tag + ': '
                    modified_str = time.strftime("Last modified: %d/%m/%Y %H:%M", time.gmtime(os.path.getmtime(os.path.join(path, name))))
                    # created_str = time.strftime("Created: %d/%m/%Y %H:%M", time.gmtime(os.path.getctime(os.path.join(path, name))));
                    note_files.append([re.sub('\.' + ext + '$', '', tag + title), os.path.join(path, name), tag, modified_str])

    note_files.sort(key=lambda item: os.path.getmtime(item[1]), reverse=True)
    return note_files


def setup_notes_list(file_list):
    # list display options
    try:
        display_modified_date = settings().get("list_options").get("display_modified_date")
        display_folder = settings().get("list_options").get("display_folder")
        display_full_path = settings().get("list_options").get("display_full_path")
    except:
        display_modified_date = True
        display_folder = True
        display_full_path = False

    indices = [0]
    if display_modified_date:
        indices.append(3)
    if display_folder:
        indices.append(2)
    if display_full_path:
        indices.append(1)

    return helpers.return_sublist(file_list, indices)


def refresh_indexes(select_path=None):
    # redraw every open Notes Index so it shows the current notes
    for window in sublime.windows():
        for view in window.views():
            if view.settings().get("notes_buffer_files") is not None:
                view.run_command("notes_buffer_refresh", {"select_path": select_path})


class NotesListCommand(sublime_plugin.ApplicationCommand):

    def run(self):
        root = get_root()
        self.notes_dir = root
        self.file_list = find_notes(self, root, [brain_dir()])
        rlist = setup_notes_list(self.file_list)
        window = sublime.active_window()
        window.show_quick_panel(rlist, self.open_note)

    def open_note(self, index):
        if index == -1:
            return
        file_path = self.file_list[index][1]
        sublime.run_command("notes_open", {"file_path": file_path})


class NotesOpenCommand(sublime_plugin.ApplicationCommand):

    def run(self, file_path):
        sublime.set_timeout(lambda: self.async_open(file_path), 0)

    def async_open(self, file_path):
        view = sublime.active_window().open_file(file_path, sublime.ENCODED_POSITION)
        f_id = file_id(file_path)
        view.settings().set("is_note", True)
        if db.get(f_id):
            view.settings().set("color_scheme", db[f_id]["color_scheme"])


class NotesOpenFolderCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.window.run_command("open_dir", {"dir": get_root()})


class NotesNewCommand(sublime_plugin.ApplicationCommand):

    def run(self, title=None, directory=None):
        self.notes_dir = get_root()
        self.base_dir = directory or self.notes_dir
        self.window = sublime.active_window()
        if title is None:
            folder = os.path.relpath(self.base_dir, self.notes_dir)
            caption = "Title" if folder == "." else u"Title (in {0})".format(folder)
            self.window.show_input_panel(caption, "", self.create_note, None, None)
        else:
            self.create_note(title)

    def create_note(self, title):
        filename = title.split("/")
        title = filename[-1]
        directory = os.path.join(self.base_dir, *filename[:-1])
        tag = os.path.relpath(directory, self.notes_dir).replace(os.sep, "/")
        if tag == ".":
            tag = ""
        if not os.path.exists(directory):
            os.makedirs(directory)

        if any(title.endswith("." + ext) for ext in settings().get("note_file_extensions")):
            ext = ""
        else:
            ext = "." + settings().get("note_save_extension")

        file = os.path.join(directory, title + ext)
        if not os.path.exists(file):
            open(file, 'w+').close()
            refresh_indexes()
        view = sublime.active_window().open_file(file)
        color_scheme = settings().get("note_color_scheme")
        if color_scheme:
            view.settings().set("color_scheme", color_scheme)
            f_id = file_id(file)
            if not db.get(f_id):
                db[f_id] = {}
            db[f_id]["color_scheme"] = color_scheme
            save_to_brain()
        self.insert_title_scheduled = False
        self.insert_title(title, tag, view)

    def insert_title(self, title, tag, view):
        if view.is_loading():
            if not self.insert_title_scheduled:
                self.insert_title_scheduled = True
                sublime.set_timeout(lambda: self.insert_title(title, tag, view), 100)
            return
        else:
            view.run_command("note_insert_title", {"title": title, "tag": tag})


class NotesEvents(sublime_plugin.EventListener):

    def on_load_async(self, view):
        root = get_root()
        if view.settings().get("is_note") or not view.file_name():
            return
        if os.path.realpath(view.file_name()).startswith(root):
            f_id = file_id(view.file_name())
            view.settings().set("is_note", True)
            if db.get(f_id) and db[f_id]["color_scheme"]:
                view.settings().set("color_scheme", db[f_id]["color_scheme"])


class NoteInsertTitleCommand(sublime_plugin.TextCommand):

    def run(self, edit, **kwargs):
        if settings().get("enable_yaml"):
            header = "---\n"
            header = header + "title: " + kwargs["title"].capitalize() + "\n"
            header = header + "date: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
            header = header + "tags: " + kwargs["tag"] + "\n"
            for yaml_el in settings().get("note_yaml"):
                header = header + yaml_el + ":\n"
            header = header + "---\n"
            self.view.insert(edit, 0, header)


class NoteChangeColorCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.colors = ["Orange", "Yellow", "Green", "GreenLight", "Blue", "BlueLight", "Purple", "Pink", "Gray", "White"]
        self.window = sublime.active_window()
        self.original_cs = self.window.active_view().settings().get("color_scheme")
        current_color = os.path.basename(self.original_cs).replace("Sticky-", "").replace(".tmTheme", "")
        if ST3:
            self.window.show_quick_panel(self.colors, self.on_select, 0, self.colors.index(current_color), self.on_highlight)
        else:
            self.window.show_quick_panel(self.colors, self.on_select, 0, self.colors.index(current_color))

    def on_select(self, index):
        global db
        if index == -1:
            self.window.active_view().settings().set("color_scheme", self.original_cs)
        else:
            try:
                path = sublime.find_resources("Sticky-" + self.colors[index] + ".tmTheme")
                path = path[0]
            except:
                path = os.path.join("Packages", "PlainNotes", "Color Schemes", "Sticky-" + self.colors[index] + ".tmTheme")

            view = self.window.active_view()
            view.settings().set("color_scheme", path)
            f_id = file_id(view.file_name())
            if not db.get(f_id):
                db[f_id] = {}
            db[f_id]["color_scheme"] = path
            save_to_brain()

    def on_highlight(self, index):
        try:
            path = sublime.find_resources("Sticky-" + self.colors[index] + ".tmTheme")
            path = path[0]
        except:
            path = os.path.join("Packages", "PlainNotes", "Color Schemes", "Sticky-" + self.colors[index] + ".tmTheme")

        self.window.active_view().settings().set("color_scheme", path)

    def is_enabled(self):
        syntax = self.window.active_view().settings().get("syntax")
        return syntax.endswith("Note.tmLanguage") or syntax.endswith("Note.sublime-syntax")


class NoteRemoveCommand(sublime_plugin.WindowCommand):

    def run(self):
        f_path = self.window.active_view().file_name()
        delete = sublime.ok_cancel_dialog('Are you sure you want to delete this note?', 'Yes')
        if delete:
            # Set the view to scratch and close it so ST doesn't prompt again.
            self.window.active_view().set_scratch(True)
            self.window.run_command("close_file")
            os.remove(f_path)

    def is_enabled(self):
        is_note = self.window.active_view().settings().get("is_note")
        if is_note:
            return is_note
        else:
            return False


class NotesMoveCommand(sublime_plugin.ApplicationCommand):
    """Move or rename a note or folder by editing its path relative to the notes folder."""

    CAPTION = "Move / rename (Enter to apply, Esc to cancel):"

    def run(self, path):
        self.root = get_root()
        self.src = os.path.normpath(path)
        self.is_dir = os.path.isdir(self.src)
        rel = os.path.relpath(self.src, self.root).replace(os.sep, "/")
        # show notes the way the Index does: without the default extension
        self.ext = "" if self.is_dir else os.path.splitext(self.src)[1]
        shown_ext = "." + settings().get("note_save_extension")
        if self.ext == shown_ext:
            rel = rel[:-len(shown_ext)]
        self.show(rel)

    def show(self, text):
        window = sublime.active_window()
        panel = window.show_input_panel(self.CAPTION, text, self.move, None, None)
        # select the name so typing renames; Home goes to the folders
        start = text.rfind("/") + 1
        end = len(text)
        if not self.is_dir and self.ext and text.endswith(self.ext):
            end -= len(self.ext)
        panel.sel().clear()
        panel.sel().add(sublime.Region(start, end))

    def fail(self, message, text):
        sublime.error_message(message)
        self.show(text)

    def move(self, text):
        parts = [p.strip() for p in text.strip().replace("\\", "/").strip("/").split("/")]
        if any(p in ("", ".", "..") for p in parts):
            return self.fail("Type a path like Folder/Name, without empty parts, '.' or '..'.", text)
        if any(p.startswith(".") for p in parts) or parts[0] == brain_dir():
            return self.fail("Hidden folders and the PlainNotes data folder can't be used.", text)

        name = parts[-1]
        if not self.is_dir and not any(name.lower().endswith("." + e) for e in settings().get("note_file_extensions")):
            name += self.ext
        dest = os.path.normpath(os.path.join(self.root, *(parts[:-1] + [name])))

        if dest == self.src:
            return
        if not os.path.exists(self.src):
            refresh_indexes()
            return sublime.error_message("This note or folder no longer exists.")
        # a case-only rename on Windows sees the source as the destination
        same_file = os.path.normcase(dest) == os.path.normcase(self.src)
        if os.path.exists(dest) and not same_file:
            return self.fail("Something already exists at " + text + ".", text)
        if self.is_dir and os.path.normcase(dest).startswith(os.path.normcase(self.src) + os.sep):
            return self.fail("A folder can't be moved into itself.", text)

        try:
            parent = os.path.dirname(dest)
            if not os.path.isdir(parent):
                os.makedirs(parent)
            os.rename(self.src, dest)
        except OSError as e:
            return self.fail("Couldn't move it: " + str(e), text)

        move_colors(self.src, dest)
        retarget_views(self.src, dest)
        refresh_indexes(dest)
        sublime.status_message("    Moved to " + os.path.relpath(dest, self.root).replace(os.sep, "/"))


def move_colors(src, dest):
    # carry saved colors over to the new path, including notes inside a moved folder
    src_id, dest_id = file_id(src), file_id(dest)
    moved = False
    for key in list(db):
        if key == src_id or key.startswith(src_id + os.sep):
            db[dest_id + key[len(src_id):]] = db.pop(key)
            moved = True
    if moved:
        save_to_brain()


def retarget_views(src, dest):
    # point open tabs of moved notes at their new location
    src_norm = os.path.normcase(src)
    for window in sublime.windows():
        for view in window.views():
            name = view.file_name()
            if not name:
                continue
            name_norm = os.path.normcase(os.path.normpath(name))
            if name_norm == src_norm:
                view.retarget(dest)
            elif name_norm.startswith(src_norm + os.sep):
                view.retarget(dest + os.path.normpath(name)[len(src):])


class NoteRenameCommand(sublime_plugin.WindowCommand):

    def run(self):
        sublime.run_command("notes_move", {"path": self.window.active_view().file_name()})

    def is_enabled(self):
        is_note = self.window.active_view().settings().get("is_note")
        if is_note:
            return is_note
        else:
            return False


def save_to_brain():
    # print("SAVING TO DISK-----------------")
    # print(db)
    with open(db_json_file, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=4, sort_keys=True)


def cleanup_brain():
    # print("Cleaning Up My Brain -----------------")
    # print(db)
    # print(len(db))
    to_delete = []
    for nfile in db:
        if not os.path.exists(os.path.join(root, nfile)):
            # print("✘" + nfile)
            to_delete.append(nfile)
    # print(to_delete)
    for x in to_delete:
        db.pop(x, None)
    # print(len(db))
    save_to_brain()


def plugin_loaded():
    global db, root, db_json_file
    # creating directory structure and files in root
    db = {}
    root = get_root()
    brain = os.path.join(root, brain_dir())
    db_json_file = os.path.join(root, brain_dir(), 'brain.json')

    if not os.path.exists(brain):
        os.makedirs(brain)

    try:
        with open(db_json_file, 'r') as f:
            db = json.load(f)
        cleanup_brain()
    except:
        db = {}

if not ST3:
    plugin_loaded()
