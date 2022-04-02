import colorsys
import json
import os
import datetime
import functools
import dataclasses
import stat
import pathlib
import os


#constants
import enum

FALLBACK_TERMINAL_WIDTH = 80

ENOENT = "ls: cannot access '%s': No such file or directory"
ENOTDIR = "ls: '%s' is not a directory"
STOPITER = "'%s': broken reparse point encountered, iteration stopped"


class Category(enum.IntEnum):
    BROKEN_LINK = enum.auto()
    DIRECTORY = enum.auto()
    SYMLINK = enum.auto()
    REPARSE_POINT = enum.auto()
    FILE = enum.auto()

    EXECUTABLE = enum.auto()
    CODE = enum.auto()
    ARCHIVE = enum.auto()
    IMAGE = enum.auto()
    VIDEO = enum.auto()
    AUDIO = enum.auto()


EXTENSION_TO_CATEGORY = {
    '.7z': Category.ARCHIVE,
    '.a': Category.ARCHIVE,
    '.apk': Category.ARCHIVE,
    '.ar': Category.ARCHIVE,
    '.bz2': Category.ARCHIVE,
    '.cab': Category.ARCHIVE,
    '.cpio': Category.ARCHIVE,
    '.deb': Category.ARCHIVE,
    '.dmg': Category.ARCHIVE,
    '.egg': Category.ARCHIVE,
    '.gz': Category.ARCHIVE,
    '.iso': Category.ARCHIVE,
    '.jar': Category.ARCHIVE,
    '.lha': Category.ARCHIVE,
    '.mar': Category.ARCHIVE,
    '.pak': Category.ARCHIVE,
    '.pea': Category.ARCHIVE,
    '.rar': Category.ARCHIVE,
    '.rpm': Category.ARCHIVE,
    '.s7z': Category.ARCHIVE,
    '.shar': Category.ARCHIVE,
    '.tar': Category.ARCHIVE,
    '.tbz2': Category.ARCHIVE,
    '.tgz': Category.ARCHIVE,
    '.tlz': Category.ARCHIVE,
    '.war': Category.ARCHIVE,
    '.whl': Category.ARCHIVE,
    '.xpi': Category.ARCHIVE,
    '.xz': Category.ARCHIVE,
    '.zip': Category.ARCHIVE,
    '.zipx': Category.ARCHIVE,

    '.bat': Category.EXECUTABLE,
    '.exe': Category.EXECUTABLE,
    '.msi': Category.EXECUTABLE,

    '.c': Category.CODE,
    '.cc': Category.CODE,
    '.class': Category.CODE,
    '.clj': Category.CODE,
    '.cljc': Category.CODE,
    '.cljs': Category.CODE,
    '.coffee': Category.CODE,
    '.cp': Category.CODE,
    '.cpp': Category.CODE,
    '.cs': Category.CODE,
    '.csproj': Category.CODE,
    '.css': Category.CODE,
    '.csx': Category.CODE,
    '.cxx': Category.CODE,
    '.d': Category.CODE,
    '.dart': Category.CODE,
    '.diff': Category.CODE,
    '.el': Category.CODE,
    '.gd': Category.CODE,
    '.go': Category.CODE,
    '.h': Category.CODE,
    '.html': Category.CODE,
    '.ipynb': Category.CODE,
    '.java': Category.CODE,
    '.js': Category.CODE,
    '.lua': Category.CODE,
    '.m': Category.CODE,
    '.m4': Category.CODE,
    '.patch': Category.CODE,
    '.php': Category.CODE,
    '.pl': Category.CODE,
    '.po': Category.CODE,
    '.py': Category.CODE,
    '.rb': Category.CODE,
    '.rs': Category.CODE,
    '.sh': Category.CODE,
    '.swift': Category.CODE,
    '.vb': Category.CODE,
    '.vcxproj': Category.CODE,
    '.vue': Category.CODE,
    '.xcodeproj': Category.CODE,
    '.xml': Category.CODE,

    '.3dm': Category.IMAGE,
    '.3ds': Category.IMAGE,
    '.ai': Category.IMAGE,
    '.bmp': Category.IMAGE,
    '.dds': Category.IMAGE,
    '.dwg': Category.IMAGE,
    '.dxf': Category.IMAGE,
    '.eps': Category.IMAGE,
    '.gif': Category.IMAGE,
    '.gpx': Category.IMAGE,
    '.jpeg': Category.IMAGE,
    '.jpg': Category.IMAGE,
    '.kml': Category.IMAGE,
    '.kmz': Category.IMAGE,
    '.max': Category.IMAGE,
    '.png': Category.IMAGE,
    '.ps': Category.IMAGE,
    '.psd': Category.IMAGE,
    '.svg': Category.IMAGE,
    '.tga': Category.IMAGE,
    '.thm': Category.IMAGE,
    '.tif': Category.IMAGE,
    '.tiff': Category.IMAGE,
    '.webp': Category.IMAGE,
    '.xcf': Category.IMAGE,

    '.aac': Category.AUDIO,
    '.aiff': Category.AUDIO,
    '.ape': Category.AUDIO,
    '.au': Category.AUDIO,
    '.flac': Category.AUDIO,
    '.gsm': Category.AUDIO,
    '.it': Category.AUDIO,
    '.m3u': Category.AUDIO,
    '.m4a': Category.AUDIO,
    '.mid': Category.AUDIO,
    '.mod': Category.AUDIO,
    '.mp3': Category.AUDIO,
    '.mpa': Category.AUDIO,
    '.pls': Category.AUDIO,
    '.ra': Category.AUDIO,
    '.s3m': Category.AUDIO,
    '.sid': Category.AUDIO,
    '.wav': Category.AUDIO,
    '.wma': Category.AUDIO,
    '.xm': Category.AUDIO,

    '.3g2': Category.VIDEO,
    '.3gp': Category.VIDEO,
    '.aaf': Category.VIDEO,
    '.asf': Category.VIDEO,
    '.avchd': Category.VIDEO,
    '.avi': Category.VIDEO,
    '.drc': Category.VIDEO,
    '.flv': Category.VIDEO,
    '.m2v': Category.VIDEO,
    '.m4p': Category.VIDEO,
    '.m4v': Category.VIDEO,
    '.mkv': Category.VIDEO,
    '.mng': Category.VIDEO,
    '.mov': Category.VIDEO,
    '.mp2': Category.VIDEO,
    '.mp4': Category.VIDEO,
    '.mpe': Category.VIDEO,
    '.mpeg': Category.VIDEO,
    '.mpg': Category.VIDEO,
    '.mpv': Category.VIDEO,
    '.mxf': Category.VIDEO,
    '.nsv': Category.VIDEO,
    '.ogg': Category.VIDEO,
    '.ogm': Category.VIDEO,
    '.ogv': Category.VIDEO,
    '.qt': Category.VIDEO,
    '.rm': Category.VIDEO,
    '.rmvb': Category.VIDEO,
    '.roq': Category.VIDEO,
    '.srt': Category.VIDEO,
    '.svi': Category.VIDEO,
    '.vob': Category.VIDEO,
    '.webm': Category.VIDEO,
    '.wmv': Category.VIDEO,
    '.yuv': Category.VIDEO,
}

#file


@dataclasses.dataclass
class File:
    dir_entry: object

    @functools.cached_property
    def name(self):
        # Path('.').name is ''
        if not self.dir_entry.name:
            return '.'

        # Any of Path('..'), Path('../..'), etc.
        if self.dir_entry.name == '..':
            return str(self.dir_entry.resolve())

        return self.dir_entry.name

    @functools.cached_property
    def size(self):
        return self.stat.st_size

    @functools.cached_property
    def size_human_readable(self):
        """Uses kibi (1024) instead of kilo (1000): KiB, MiB ..."""
        size = self.size

        if size < 1024:
            return '%d' % size

        for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
            if size < 1024:
                if size < 9:
                    return '%.1f%s' % (size, unit)
                return '%.0f%s' % (size, unit)
            size /= 1024

        return '%.1f%s' % (size, 'Y')

    @functools.cached_property
    def extension(self):
        return os.path.splitext(self.name)[1].lower()

    @functools.cached_property
    def real_path(self):
        return os.path.realpath(self.dir_entry)

    @functools.cached_property
    def relative_path(self):
        return os.path.relpath(self.dir_entry)

    @functools.cached_property
    def is_dir(self):
        if isinstance(self.dir_entry, pathlib.Path):
            return self.stat.st_mode & stat.S_IFDIR
        return self.dir_entry.is_dir(follow_symlinks=False)

    @functools.cached_property
    def is_symlink(self):
        return self.dir_entry.is_symlink()

    @functools.cached_property
    def attributes(self):
        """Windows file attributes"""
        return self.stat.st_file_attributes

    @functools.cached_property
    def filemode(self):
        return stat.filemode(self.stat.st_mode)

    @functools.cached_property
    def is_reparse(self):
        if os.name == 'posix':
            return False

        # Symlinks also have the REPARSE_POINT attribute
        # but reparse points != symlinks
        return bool(
            self.attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
            and not self.is_symlink
        )

    @functools.cached_property
    def is_broken(self):
        """Checks if symlink or a reparse point is broken"""
        if not self.is_symlink and not self.is_reparse:
            return False
        return not os.path.exists(self.real_path)

    @functools.cached_property
    def target(self):
        """Returns symlink/reparse point target path"""
        if not self.is_symlink and not self.is_reparse:
            return None

        relative_pointer = os.path.relpath(self.real_path)
        if relative_pointer.startswith('..'):
            return self.real_path

        return relative_pointer

    @functools.cached_property
    def last_modified_ts(self):
        """Returns timestamp of last file modification"""
        return self.stat.st_mtime

    @functools.cached_property
    def last_modified_str(self):
        """Returns string representation of when the file was last modified
           For example: "May  4 06:55", "Apr 20 13:37"
        """
        date = datetime.datetime.fromtimestamp(self.last_modified_ts)
        month = date.strftime('%B')
        day = date.strftime('%d')
        time = date.strftime('%H:%M')
        if day[0] == '0':
            day = day.replace('0', ' ', 1)
        return '%s %s %s' % (month[:3], day, time,)

    @functools.cached_property
    def stat(self):
        """Returns the appropriate dir_entry.stat based on its type"""
        if isinstance(self.dir_entry, pathlib.Path):
            # We need lstat if we're using pathlib to detect reparse points
            return self.dir_entry.lstat()
        return self.dir_entry.stat(follow_symlinks=False)

    @functools.cached_property
    def parent(self):
        """Must only be used if File is created from Path (when using globs)"""
        return File(self.dir_entry.parent)

    def unwrap_parents(self):
        """For `a/b/c/file` yields (c, b, a)"""
        if isinstance(self.dir_entry, os.DirEntry):
            for parent in reversed(self.relative_path.split(os.sep)[:-1]):
                yield parent
        else:
            cur_par = self.parent
            while cur_par.name != '.':
                yield cur_par
                cur_par = cur_par.parent

    @functools.cached_property
    def hidden(self):
        """Checks if filename starts with a '.'
        If on Windows, also checks whether file attributes are set to hidden
        """
        hidden = self.name[0] == '.'
        if os.name == 'nt':
            return hidden or self.attributes & stat.FILE_ATTRIBUTE_HIDDEN
        return hidden

    @functools.cached_property
    def category(self):
        """Used for sorting by category and choosing the appropriate color"""
        if self.is_broken:
            return Category.BROKEN_LINK
        if self.is_symlink:
            return Category.SYMLINK
        if self.is_reparse:
            return Category.REPARSE_POINT
        if self.is_dir:
            return Category.DIRECTORY

        return EXTENSION_TO_CATEGORY.get(self.extension, Category.FILE)
#color_scheme


COLOR_SCHEME = {
    Category.FILE: ('green', None, []),
    Category.DIRECTORY: ('blue', None, ['bold']),
    Category.SYMLINK: ('black', 'cyan', ['underline']),
    Category.REPARSE_POINT: ('black', 'cyan', ['underline']),
    Category.BROKEN_LINK: ('black', 'red', []),
    Category.ARCHIVE: ('red', None, []),
    Category.EXECUTABLE: ('red', None, ['bold']),
    Category.CODE: ('magenta', None, []),
    Category.IMAGE: ('yellow', None, []),
    Category.VIDEO: ('yellow', None, ['bold']),
    Category.AUDIO: ('yellow', None, []),
}

SIZE = {
    'start_color': '#00ff00',
    'end_color': '#ff0000',
    'maxsize': 1073741824,
    'thresholds': [0.0625, 0.125, 0.1875, 0.25, 0.375, 0.5, 0.75, 1]
}


# colors
SIZE_STEPS = None
SIZE_GRADIENT = None

COLORS = {
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'white': 37
}

BG_COLORS = {
    'black': 40,
    'red': 41,
    'green': 42,
    'yellow': 43,
    'blue': 44,
    'magenta': 45,
    'cyan': 46,
    'white': 47
}

RESET = 0
ATTRIBUTES = {
    'bold': 1,
    'dim': 2,
    'italic': 3,
    'underline': 4,
    'blink': 5,
    'reverse': 7,
    'hidden': 8
}

# 16 colors
ANSI = '\033[%dm'
# 256 colors, unused
FG08 = '\033[38;5;%dm'
BG08 = '\033[48;5;%dm'
# RGB
FG24 = '\033[38;2;%d;%d;%dm'
BG24 = '\033[48;2;%d;%d;%dm'

class color:
  def init(long_listing=False):
      """If we're not using ConEmu or Windows Terminal we have to call
      os.system('color') to enable colors and eliminate line wrapping
      """
      is_conemu = 'CONEMUDIR' in os.environ
      is_windows_terminal = 'WT_SESSION' in os.environ
      if os.name == 'nt' and not (is_conemu or is_windows_terminal):
          os.system('color')
  
      lss_path = os.path.dirname(os.path.realpath(__file__))
      custom_path = os.path.join(lss_path, 'lss_custom.json')
  
      if os.path.exists(custom_path):
          with open(custom_path) as file:
              custom = json.load(file)
              for key, value in custom['categories'].items():
                  COLOR_SCHEME[Category[key.upper()]] = value
              for key, value in custom['size'].items():
                  SIZE[key] = value
  
      # Generate gradients only if we're using long listing mode
      if long_listing:
          global SIZE_STEPS
          global SIZE_GRADIENT
  
          SIZE_STEPS = [SIZE['maxsize'] * i for i in SIZE['thresholds']]
          start_rgb = tuple(i/255 for i in hex_to_rgb(SIZE['start_color']))
          end_rgb = tuple(i/255 for i in hex_to_rgb(SIZE['end_color']))
  
          SIZE_GRADIENT = list(
              make_gradient(start_rgb, end_rgb, len(SIZE_STEPS) - 1)
          )
  
  
  def sizecolor(size):
      if size >= SIZE_STEPS[-1]:
          return SIZE_GRADIENT[-1]
  
      for i, step in enumerate(SIZE_STEPS):
          if size < step:
              return SIZE_GRADIENT[i]
  
  

  
  
  def fmt(string, fg=None, bg=None, attributes=None):
      if not attributes:
          attributes = tuple()
  
      if isinstance(fg, str):
          fg_fmt = ANSI % COLORS[fg] if fg else ''
      else:
          fg_fmt = FG24 % (fg[0], fg[1], fg[2]) if fg else ''
  
      if isinstance(bg, str):
          bg_fmt = ANSI % BG_COLORS[bg] if bg else ''
      else:
          bg_fmt = BG24 % (bg[0], bg[1], bg[2]) if bg else ''
  
      attrs_fmt = ''.join(ANSI % ATTRIBUTES[attr] for attr in attributes)
      return '%s%s%s%s%s' % (bg_fmt, fg_fmt, attrs_fmt, string, ANSI % RESET)

  def fmt_cat(string, category):
      return color.fmt(string, *COLOR_SCHEME[category])
  
  def hex_to_rgb(code):
      code = code.lstrip('#')
      if len(code) != 6:
          raise ValueError
  
      return int(code[:2], 16), int(code[2:4], 16), int(code[4:], 16)
  
  
  def make_gradient(start_rgb, end_rgb, steps):
      start = colorsys.rgb_to_hsv(*start_rgb)
      end = colorsys.rgb_to_hsv(*end_rgb)
      reverse = False
  
      if end[0] < start[0]:
          start, end = end, start
          reverse = True
  
      dist_forward = end[0] - start[0]
      dist_backwards = start[0] + (1 - end[0])
  
      if dist_backwards < dist_forward:
          step_h = -dist_backwards / steps
      else:
          step_h = dist_forward / steps
  
      step_s = (end[1] - start[1]) / steps
      step_v = (end[2] - start[2]) / steps
  
      step_iter = range(steps+1) if not reverse else reversed(range(steps+1))
      for i in step_iter:
          h = start[0] + step_h * i
          if h < 0:
              h = 1 + h
          s = start[1] + step_s * i
          v = start[2] + step_v * i
  
          yield tuple(i * 255 for i in colorsys.hsv_to_rgb(h, s, v))
import os
import sys
# icons
class icons:
  FILE = '📝'
  DIR = '📁'
  SUBDIR = '📂'
  
  SYMLINK_FILE = '🔗'
  SYMLINK_DIR = '🔗'
  SYMLINK_PTR = '➡️'
  
  ARCHIVE = '📦'
  AUDIO = '🎵'
  CONFIG = '⚙️'
  IMAGE = '🖼️'
  SHELL = '▶️'
  SUBL = '✏️'
  VIDEO = '⏯️'
  WIN_EXECUTABLE = '❄️'
  
  C_LANG = '©️'
  CPP = '©️+'
  CS = '©️#'
  CLOJURE = '☯️'
  PYTHON = '🐍'
  
  EXTENSIONS = {
      '.apk': '🎁',
      '.c': C_LANG,
      '.h': C_LANG,
      '.hpp': CPP,
      '.hxx': CPP,
      '.cfg': CONFIG,
      '.clj': CLOJURE,
      '.cljc': CLOJURE,
      '.cljs': CLOJURE,
      '.coffee': '☕',
      '.cc': CPP,
      '.cp': CPP,
      '.cpp': CPP,
      '.cxx': CPP,
      '.cs': CS,
      'csproj': CS,
      '.csx': CS,
      '.css': '💼',
      '.d': '🧳',
      '.dart': '🏹',
      '.db': '🗃️',
      '.ds_store': '⚙️',
      '.ipynb': PYTHON,
      '.md': '📕',
      '.py': PYTHON,
      '.pyc': PYTHON,
      '.psd': '🖼️',
      '.rs': '🪙',
      '.vue': '📜',
      '.sln': "🗄️",
      '.sql': "⏹️",
      '.sqlite3': "⏹️",
      '.sublime_keymap': SUBL,
      '.sublime_package': SUBL,
      '.sublime_settings': SUBL,
      '.sublime_theme': SUBL,
      '.txt': '📄',
      'ps1': SHELL,
      'sh': SHELL,
      'shell': SHELL,
  
      # Everything below needs to be in sync with EXTENSION_TO_CATEGORY
      '.7z': ARCHIVE,
      '.a': ARCHIVE,
      '.ar': ARCHIVE,
      '.bz2': ARCHIVE,
      '.cab': ARCHIVE,
      '.cpio': ARCHIVE,
      '.deb': ARCHIVE,
      '.dmg': ARCHIVE,
      '.egg': ARCHIVE,
      '.gz': ARCHIVE,
      '.iso': ARCHIVE,
      '.jar': ARCHIVE,
      '.lha': ARCHIVE,
      '.mar': ARCHIVE,
      '.pak': ARCHIVE,
      '.pea': ARCHIVE,
      '.rar': ARCHIVE,
      '.rpm': ARCHIVE,
      '.s7z': ARCHIVE,
      '.shar': ARCHIVE,
      '.tar': ARCHIVE,
      '.tbz2': ARCHIVE,
      '.tgz': ARCHIVE,
      '.tlz': ARCHIVE,
      '.war': ARCHIVE,
      '.whl': ARCHIVE,
      '.xpi': ARCHIVE,
      '.xz': ARCHIVE,
      '.zip': ARCHIVE,
      '.zipx': ARCHIVE,
  
      '.bat': WIN_EXECUTABLE,
      '.exe': WIN_EXECUTABLE,
      '.msi': WIN_EXECUTABLE,
  
      '.3dm': IMAGE,
      '.3ds': IMAGE,
      '.ai': IMAGE,
      '.bmp': IMAGE,
      '.dds': IMAGE,
      '.dwg': IMAGE,
      '.dxf': IMAGE,
      '.eps': IMAGE,
      '.gif': IMAGE,
      '.gpx': IMAGE,
      '.jpeg': IMAGE,
      '.jpg': IMAGE,
      '.kml': IMAGE,
      '.kmz': IMAGE,
      '.max': IMAGE,
      '.png': IMAGE,
      '.ps': IMAGE,
      '.svg': IMAGE,
      '.tga': IMAGE,
      '.thm': IMAGE,
      '.tif': IMAGE,
      '.tiff': IMAGE,
      '.webp': IMAGE,
      '.xcf': IMAGE,
  
      '.aac': AUDIO,
      '.aiff': AUDIO,
      '.ape': AUDIO,
      '.au': AUDIO,
      '.flac': AUDIO,
      '.gsm': AUDIO,
      '.it': AUDIO,
      '.m3u': AUDIO,
      '.m4a': AUDIO,
      '.mid': AUDIO,
      '.mod': AUDIO,
      '.mp3': AUDIO,
      '.mpa': AUDIO,
      '.pls': AUDIO,
      '.ra': AUDIO,
      '.s3m': AUDIO,
      '.sid': AUDIO,
      '.wav': AUDIO,
      '.wma': AUDIO,
      '.xm': AUDIO,
  
      '.3g2': VIDEO,
      '.3gp': VIDEO,
      '.aaf': VIDEO,
      '.asf': VIDEO,
      '.avchd': VIDEO,
      '.avi': VIDEO,
      '.drc': VIDEO,
      '.flv': VIDEO,
      '.m2v': VIDEO,
      '.m4p': VIDEO,
      '.m4v': VIDEO,
      '.mkv': VIDEO,
      '.mng': VIDEO,
      '.mov': VIDEO,
      '.mp2': VIDEO,
      '.mp4': VIDEO,
      '.mpe': VIDEO,
      '.mpeg': VIDEO,
      '.mpg': VIDEO,
      '.mpv': VIDEO,
      '.mxf': VIDEO,
      '.nsv': VIDEO,
      '.ogg': VIDEO,
      '.ogm': VIDEO,
      '.ogv': VIDEO,
      '.qt': VIDEO,
      '.rm': VIDEO,
      '.rmvb': VIDEO,
      '.roq': VIDEO,
      '.srt': VIDEO,
      '.svi': VIDEO,
      '.vob': VIDEO,
      '.webm': VIDEO,
      '.wmv': VIDEO,
      '.yuv': VIDEO,
  }


ash = "is-ash-shell"
Ash = "ash-shell"
cwd = "ash-shell-path"
cwd = str(cwd)

# ls
import argparse
import collections
import functools
import os
import pathlib
import sys
if len(sys.argv) == 2:
  if sys.argv[1].startswith("-") == False:
    cwd = sys.argv[1]


def prettify(file, args):
    pretty = file.name

    if args.quote:
        pretty = '%s%s%s' % (args.quote, pretty, args.quote)

    if not args.show_icons:
        return pretty

    if file.is_symlink or file.is_reparse:
        icon = icons.SYMLINK_DIR if file.is_dir else icons.SYMLINK_FILE

        if args.show_targets:
            arrow = '->' if not args.show_icons else icons.SYMLINK_PTR
            pretty = '%s %s %s' % (pretty, arrow, file.target)

    elif file.is_dir:
        icon = icons.DIR
    else:
        icon = icons.EXTENSIONS.get(file.extension, icons.FILE)

    return '%s %s' % (icon, pretty)


def colorize(file, args):
    if not args.show_colors:
        return prettify(file, args)
    return color.fmt_cat(prettify(file, args), file.category)


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return FALLBACK_TERMINAL_WIDTH


def get_files(pattern, return_hidden=False):
    if '*' in pattern:
        files = (File(path) for path in pathlib.Path().glob(pattern))
    else:
        try:
            files = (File(dir_entry) for dir_entry in os.scandir(pattern))
        except FileNotFoundError:
            print(ENOENT % pattern)
            sys.exit(2)  # ENOENT

    if not return_hidden:
        files = (file for file in files if not file.hidden)
    return files


# Change to @functools.cache once Python 3.9 releases
@functools.lru_cache(maxsize=None)
def get_row_col(i, rows):
    row = i % rows
    return row, (i-row) // rows


def format_rows(files, file_count, columns, terminal_width, args):
    if file_count % columns != 0:
        row_count = (file_count // columns) + 1
    else:
        row_count = file_count // columns

    rows = [[] for row in range(row_count)]
    column_widths = [0] * columns

    for i in range(file_count):
        _, col = get_row_col(i, row_count)
        name_length = len(prettify(files[i], args))

        if name_length > column_widths[col]:
            column_widths[col] = name_length

    row_width = sum(column_widths) + (len(column_widths) - 1) * args.col_sep
    if row_width >= terminal_width:
        return None

    for i in range(file_count):
        row, col = get_row_col(i, row_count)
        whitespace = ' ' * (column_widths[col] - len(prettify(files[i], args)))
        rows[row].append('%s%s' % (colorize(files[i], args), whitespace))

    return rows


def sort_files(files, args):
    # Files on Linux are not guaranteed to be sorted alphabetically
    if os.name == 'posix':
        files.sort(key=lambda x: x.name.lower())

    if args.sort in ('size', 'S'):
        files.sort(key=lambda x: x.size, reverse=True)
    elif args.sort in ('time', 't'):
        files.sort(key=lambda x: x.last_modified_ts, reverse=True)
    elif args.sort in ('extension', 'X'):
        files.sort(key=lambda x: x.extension)
    elif args.sort in ('category', 'c'):
        files.sort(key=lambda x: x.category)

    if args.reverse:
        files.reverse()


def process_files(files, args):
    sort_files(files, args)

    if args.long_listing or args.columns == 1:
        columns = 1
    else:
        terminal_width = get_terminal_width()
        file_count = len(files)
        columns = 2 if not args.columns else args.columns

    # If columns argument is set, we go backwards immediately
    going_backwards = bool(args.columns)
    while columns > 1:
        rows = format_rows(files, file_count, columns, terminal_width, args)
        if going_backwards and rows:
            break
        if not rows:
            going_backwards = True

        columns = columns * 2 if not going_backwards else columns - 1

    # Outputting files in a list
    if columns == 1:
        if args.long_listing:
            if args.bytes:
                sizes = [str(file.size) for file in files]
            else:
                sizes = [file.size_human_readable for file in files]
            size_align = len(max(sizes, key=len))

            for i in range(len(files)):
                size_s = sizes[i]
                ws_align = ' ' * (size_align - len(sizes[i]))

                if args.show_colors:
                    size_s = color.color.fmt(size_s, color.sizecolor(files[i].size))

                line = ['%s%s' % (ws_align, size_s),
                        files[i].last_modified_str,
                        colorize(files[i], args)]

                if args.filemode:
                    line.insert(0, files[i].filemode)

                print(' '.join(line))
        else:
            for file in files:
                print(colorize(file, args))

    # Outputting files in columns
    else:
        separator = ' ' * args.col_sep
        for row in rows:
            print(separator.join(row))


def process_glob(files, args):
    parents = collections.defaultdict(list)
    for file in files:
        parents[str(file.parent.dir_entry)].append(file)

    iterable = reversed(parents.items()) if args.reverse else parents.items()
    for parent_name, children in iterable:
        if not args.all:
            for child_file in children:
                if any(p.hidden for p in child_file.unwrap_parents()):
                    continue

        if parent_name != '.':
            print('%s:' % parent_name)

        process_files(children, args)


def process_tree(files, args, from_depths):
    sort_files(files, args)
    depth = len(list(files[0].unwrap_parents()))

    for file in files:
        is_last = file == files[-1]

        if file.is_dir and is_last:
            from_depths.discard(depth)
        elif file.is_dir:
            from_depths.add(depth)

        prefix = ''
        for i in range(depth):
            if i in from_depths:
                prefix += '│  '
            else:
                prefix += '   '

        if is_last:
            prefix += '└──'
        else:
            prefix += '├──'

        fmt_str = '%s%s' % (prefix, colorize(file, args))

        if not file.is_dir or file.is_reparse or file.is_symlink:
            print(fmt_str)

        if file.is_dir and not (file.is_reparse or file.is_symlink):
            try:
                dir_files = list(get_files(file.real_path, args.all))
                print(fmt_str)
                if dir_files:
                    process_tree(dir_files, args, from_depths)
            except PermissionError:
                print('%s %s' % (fmt_str, '[error opening dir]'))


def process_pattern(pattern, args):
    if args.tree:
        try:
            os.chdir(os.path.join(os.getcwd(), pattern))
        except FileNotFoundError:
            print(ENOENT % pattern)
            sys.exit(2)  # ENOENT
        except NotADirectoryError:
            print(ENOTDIR % pattern)
            sys.exit(20)  # ENOTDIR

        if args.show_colors:
            print(color.fmt_cat(pattern, Category.DIRECTORY))
        else:
            print(pattern)

        process_tree(list(get_files('.', args.all)), args, {0})

    elif '*' in pattern:
        generator = get_files(pattern, args.all)
        files = []
        while True:
            try:
                files.append(next(generator))
            # Broken reparse points encountered by Path().glob() raise OSError
            except OSError as ex:
                if ex.args[0] == 2:
                    print(STOPITER % pattern)
            except StopIteration:
                break

        process_glob(files, args)

    else:
        files = list(get_files(pattern, args.all))
        process_files(files, args)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('paths', nargs='*', default=tuple('.'))
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='do not ignore hidden files'
    )
    parser.add_argument(
        '-l', '--long-listing',
        action='store_true',
        help='use a long listing format'
    )
    parser.add_argument(
        '-t', '--tree',
        action='store_true',
        help='list contents of directories in a tree-like format'
    )
    parser.add_argument(
        '-b', '--bytes',
        action='store_true',
        help='with -l: print size in bytes'
    )
    parser.add_argument(
        '-f', '--filemode',
        action='store_true',
        help='with -l: print file mode'
    )
    parser.add_argument(
        '--sort',
        choices=('size', 'time', 'extension', 'category'),
        help='sort by WORD instead of name'
    )
    parser.add_argument(
        '-s',
        dest='sort',
        choices=('S', 't', 'X', 'c'),
        help='shorthand for --sort'
    )
    parser.add_argument(
        '-c', '--columns',
        metavar='AMOUNT',
        type=int,
        help='set maximum amount of columns'
    )
    parser.add_argument(
        '-r', '--reverse',
        action='store_true',
        help='reverse file order'
    )
    parser.add_argument(
        '-q', '--quote',
        default='',
        help='add value as a quote for filenames that contain a space'
    )
    parser.add_argument(
        '--col-sep',
        help='set amount of whitespace between columns',
        metavar='AMOUNT',
        type=int,
        default=2
    )
    parser.add_argument(
        '--no-colors',
        action='store_false',
        dest='show_colors',
        help='disable colors'
    )
    parser.add_argument(
        '--no-icons',
        action='store_false',
        dest='show_icons',
        help='disable icons'
    )
    parser.add_argument(
        '--no-targets',
        action='store_false',
        dest='show_targets',
        help='do not print symlink targets'
    )

    args = parser.parse_args()

    if args.columns and args.columns < 1:
        print('--columns: amount should be >=1')
        sys.exit(-1)
    if args.col_sep < 0:
        print('--col-sep: amount should be >=0')
        sys.exit(-1)

    if not sys.stdout.isatty():
        args.columns = 1
        args.show_colors = False
        args.show_icons = False
        args.show_targets = False

    if args.show_colors:
        color.init(args.long_listing)

    for pattern in args.paths:
        if len(args.paths) > 1 and '*' not in pattern:
            print('%s:' % pattern)
        

        pattern = cwd
        if pattern.endswith("/") == False:
          pattern += "/"
        process_pattern(pattern, args)


if __name__ == '__main__':
    main()