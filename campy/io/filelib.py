"""
This file exports a standardized set of tools for working with
files. The library offers at least some portability across the
file systems used in the three supported platforms: Mac OSX,
Windows, and Linux.  Directory and search paths are allowed to
contain separators in any of the supported styles, which usually
makes it possible to use the same code on different platforms.

Note: Several of the functions that lived in CPP's version of this
library are removed, to force students to learn the proper builtin
pathlib library. The compatability is listed here::

    def create_directory(path):
        _Path(path).mkdir()

    def create_directory_path(path):
        _Path(path).mkdir(path, parents=True)

    def default_extension(path, ext):
        p = _Path(path)
        if ext.startswith('*') or not p.suffix:
            return p.with_suffix(ext)

    def delete_file(path):
        return os.remove(path)

TODO more
"""
from pathlib import Path as _Path, PurePath as _PurePath
import campy.private.platform as _platform

def expand_pathname(path):
    pass

def file_exists(path):
    pass

def find_on_path(path, filename):
    pass

def get_current_directory():
    pass

def get_directory_path_separator():
    pass

def get_extension(path):
    pass

def get_head(path):
    pass

def get_root(path):
    pass

def get_search_path_separator(path):
    pass

def get_tail(path):
    pass

def get_temp_directory():
    pass

def is_directory(path):
    pass

def is_file(path):
    pass

def is_symbolic_link(path):
    pass

def list_directory(path):
    pass

def match_filename_pattern(path):
    pass

def open_file(path):
    pass

def open_file_dialog(title):
    pass

def open_on_path(path):
    pass

def prompt_user_for_file(prompt="", reprompt=""):
    pass

def read_entire_file(stream, lines):
    pass

def rename(old, new):
    pass

def rewindStream(input):
    pass

def set_current_directory(path):
    pass

def write_entire_file(path):
    pass


# '''
# This file exports a standardized set of tools for working with
# files.  The library offers at least some portability across the
# file systems used in the three supported platforms: Mac OSX,
# Windows, and Linux.  Directory and search paths are allowed to
# contain separators in any of the supported styles, which usually
# makes it possible to use the same code on different platforms.
# '''
# import platform
# import os
# import exceptions

# if(os.name == "posix"): import pwd

# def expandPathname(filename):
#   '''
#   Expands a filename into a canonical name for the platform.

#   @type filename: string
#   @param filename: filename to expand
#   @rtype: string
#   '''
#   if(filename == ""): return ""
#   length = len(filename)
#   if(os.name == "posix"):
#       strPos = 1
#       while(strPos < length \
#           and filename[strPos] != "\\" \
#           and filename[strPos] != "/"):
#           strPos += 1

#       homedir = None
#       if(strPos == 1):
#           homedir = os.getenv("HOME")
#           if(homedir == None): homedir = pwd.getpwuid(os.getuid()).pw_dir
#       else:
#           pw = pwd.getpwnam(filename[1:strPos])
#           if(pw == None):
#               raise exception.StandardError
#           homedir = pw.pw_dir

#       filename = homedir + filename[strPos:]
#       length = len(filename)

#       for i in range(length):
#           if(filename[i] == "\\"):
#               filename = filename[:i] + "/" + filename[i+1:]

#   else:
#       for i in range(length):
#           if(filename[i] == "/"):
#               filename = filename[:i] + "\\" + filename[i+1:]

#   return filename

# def openFile(filename, binary=False):
#   '''
#   Opens the filestream stream using the specified
#   filename.  This function is similar to the open
#   method of the stream classes, but uses a C++ string
#   object instead of the older C-style string.  If the operation
#   succeeds, openFile returns true;
#   if it fails, openFile sets the failure flag in the
#   stream and returns false.

#   @type filename: string
#   @param filename: file to open
#   @type binary: boolean
#   @param binary: open file in binary mode on Windows
#   @rtype: file
#   '''
#   mode = "r+"
#   if(binary):
#       mode = "r+b"

#   file = None

#   try:
#       file = open(expandPathname(filename), mode)
#   except IOError:
#       file = None

#   return file

# def promptUserForFile(prompt, binary=False):
#   '''
#   Asks the user for the name of a file.  The file is opened using
#   the reference parameter stream, and the function
#   returns the name of the file.  If the requested file cannot be
#   opened, the user is given additional chances to enter a valid file.
#   The optional prompt argument provides an input prompt
#   for the user.

#   @type prompt: string
#   @param prompt: file prompt text
#   @type binary: boolean
#   @param binary: open file in binary mode on Windows
#   @rtype: file
#   '''
#   while(True):
#       filename = raw_input(prompt)
#       file = openFile(filename, binary)
#       if(file != None): return file
#       print("Unable to open that file. Try again.")
#       if(prompt == ""): prompt = "Filename: "

def open_file_dialog(title = "Open File", mode="load", path = "", binary=False):
  '''
  Opens a dialog that allows the user to choose the file.  The
  title parameter is displayed in the dialog title.
  The path parameter is used to set the working directory;
  if path does not appear, openFileDialog
  uses the current directory.

  @type title: string
  @param title: title of dialog box
  @type mode: string
  @param mode: mode of dialog box
  @type binary: boolean
  @param binary: open file in binary mode on windows
  @rtype: file
  '''
  filename = _platform.Platform().openFileDialog(title, mode, path)
  if(filename == ""): return None
  return filename

# def readEntireFile(file):
#   '''
#   Reads the entire contents of the specified input stream into the
#   string vector lines.  The client is responsible for
#   opening and closing the stream.  The vector can be either an STL
#   vector or a Vector as defined in the
#   Stanford C++ libraries.

#   @type file: file
#   @param file: file to read
#   @rtype: [string]
#   @return: list of strings representing all lines in the file
#   '''
#   return file.readlines()

# def getRoot(filename):
#   '''
#   Returns the root of filename.  The root consists
#   of everything in filename up to the last dot and
#   the subsequent extension.  If no dot appears in the final component
#   of the filename, getRoot returns the entire name.

#   @type filename: string
#   @param filename: filename to get root from
#   @rtype: string
#   '''
#   dot = -1
#   length = len(filename)
#   for i in range(length):
#       if(filename[i] == "."): dot = i
#       if(filename[i] == "/" or filename[i] == "\\"): dot = -1

#   if(dot == -1):
#       return filename
#   else:
#       return filename[:dot]

# def getExtension(filename):
#   '''
#   Returns the extension of filename.  The extension
#   consists of the separating dot and all subsequent characters.
#   If no dot exists in the final component, getExtension
#   returns the empty string.  These semantics ensure that concatenating
#   the root and the extension always returns the original filename.

#   @type filename: string
#   @param filename: filename to get extension from
#   @rtype: string
#   '''
#   dot = -1
#   length = len(filename)
#   for i in range(length):
#       if(filename[i] == "."): dot = i
#       if(filename[i] == "/" or filename[i] == "\\"): dot = -1

#   if(dot == -1):
#       return ""
#   else:
#       return filename[dot:]

# def getHead(filename):
#   '''
#   Returns all but the last component of a path name.  The components
#   of the path name can be separated by any of the directory path
#   separators (forward or reverse slashes).  The special cases are
#   illustrated by the following examples:

#       - getHead("a/b")  = "a"     getTail("a/b")   = "b"
#       - getHead("a")    = ""      getTail("a")     = "a"
#       - getHead("/a")   = "/"     getTail("/a")    = "a"
#       - getHead("/")    = "/"     getTail("/")     = ""

#   @type filename: string
#   @param filename: filename to get head from
#   @rtype: string
#   '''
#   slash = -1
#   length = len(filename)
#   for i in range(length):
#       if(filename[i] == "/" or filename[i] == "\\"):
#           slash = i

#   if(slash == -1):
#       return ""
#   elif(slash == 0):
#       return "/"
#   else:
#       return filename[0:slash]

# def getTail(filename):
#   '''
#   Returns the last component of a path name.  The components of the
#   path name can be separated by any of the directory path separators
#   (forward or reverse slashes).  For details on the interpretation of
#   special cases, see the comments for the getHead function.

#   @type filename: string
#   @param filename: filename to get tail from
#   @rtype: string
#   '''
#   slash = -1
#   length = len(filename)
#   for i in range(length):
#       if(filename[i] == "/" or filename[i] == "\\"):
#           slash = i

#   if(slash == -1):
#       return filename
#   else:
#       return filename[slash+1:]

# def defaultExtension(filename, ext):
#   '''
#   Adds an extension to a file name if none already exists.  If the
#   extension argument begins with a leading *,
#   any existing extension in filename is replaced by
#   ext.

#   @type filename: string
#   @param filename: filename to change extension on
#   @type ext: string
#   @param ext: new extension
#   @rtype: string
#   '''
#   force = (ext[0] == "*")
#   if(force): ext = ext[1:]
#   dot = -1
#   length = len(filename)
#   for i in range(length):
#       if(filename[i] == "."): dot = i
#       if(filename[i] == "/" or filename[i] == "\\"): dot = -1

#   if(dot == -1):
#       force = True
#       dot = length

#   if(force):
#       return filename[0:dot] + ext
#   else:
#       return filename

# def openOnPath(path, filename, binary = False):
#   '''
#   Opens a file using a search path.  If openOnPath
#   is successful, it returns the first path name on the search path
#   for which stream.open succeeds.  The path
#   argument consists of a list of directories that are prepended to the
#   filename, unless filename begins with an absolute
#   directory marker, such as / or ~.
#   The directories in the search path may be separated either
#   by colons (Unix or Mac OS) or semicolons (Windows).  If the file
#   cannot be opened, the failure bit is set in the stream
#   parameter, and the openOnPath function returns the
#   empty string.

#   @type path: string
#   @param path: search paths to use when finding filename
#   @type filename: string
#   @param filename: file to search for
#   @type binary: boolean
#   @param binary: open in binary mode on windows
#   @rtype: file
#   '''
#   paths = splitPath(path)
#   for dir in paths:
#       pathname = dir + "/" + filename
#       file = openFile(pathname, binary)
#       if(file != None): return file

#   return None

# def findOnPath(path, filename):
#   '''
#   Returns the canonical name of a file found using a search path.
#   The findOnPath function is similar to
#   openOnPath, except that it doesn't actually
#   return an open stream.  If no matching file is found,
#   findOnPath returns the empty string.

#   @type path: string
#   @param path: search paths to use when finding filename
#   @type filename: string
#   @param filename: file to search for
#   @rtype: string
#   '''
#   file = openOnPath(path, filename)
#   if(file == None):
#       return None

#   file.close()
#   return file.name

# def deleteFile(filename):
#   '''
#   Deletes the specified file.  Errors are reported by calling
#   error.

#   @type filename: string
#   @param filename: file to delete
#   @rtype: void
#   '''
#   os.remove(expandPathname(filename))

# def renameFile(oldname, newname):
#   '''
#   Renames a file.  Errors are reported by calling
#   error in the implementation.

#   @type oldname: string
#   @param oldname: file to rename
#   @type newname: string
#   @param newname: new name for file
#   @rtype: void
#   '''
#   oldname = expandPathname(oldname)
#   newname = expandPathname(newname)
#   os.rename(oldname, newname)

# def createDirectory(path):
#   '''
#   Creates a new directory for the specified path.  The
#   createDirectory function does not report an error if
#   the directory already exists.  Unlike createDirectoryPath,
#   createDirectory does not create missing directories
#   along the path.  If some component of path does
#   not exist, this function signals an error.

#   @type path: string
#   @param path: path to create new directory on
#   @rtype: void
#   '''
#   os.mkdir(path)

# def createDirectoryPath(path):
#   '''
#   Creates a new directory for the specified path.   If intermediate
#   components of path do not exist, this function creates
#   them as needed.

#   @type path: string
#   @param path: path to created new directory on
#   @rtype: void
#   '''
#   cp = 1
#   if(path == ""): return
#   while(true):
#       cp = path.find(os.pardir, cp+1)
#       if(cp == -1): break
#       os.makedirs(path[:cp - 1])
#   os.makedirs(path)

# def fileExists(filename):
#   '''
#   Returns true if the specified file exists.

#   @type filename: string
#   @param filename: file to check existence of
#   @rtype: boolean
#   '''
#   return os.path.exists(filename)

# def isFile(filename):
#   '''
#   Returns true if the specified file is a regular file.

#   @type filename: string
#   @param filename: file to check status of
#   @rtype: boolean
#   '''
#   return os.path.isfile(filename)

# def isSymbolicLink(filename):
#   '''
#   Returns true if the specified file is a symbolic link.

#   @type filename: string
#   @param filename: file to check status of
#   @rtype: boolean
#   '''
#   return os.path.islink(filename)

# def isDirectory(filename):
#   '''
#   Returns true if the specified file is a directory.

#   @type filename: string
#   @param filename: file to check status of
#   @rtype: boolean
#   '''
#   return os.path.isdir(filename)

# def setCurrentDirectory(path):
#   '''
#   Changes the current directory to the specified path.

#   @type path: string
#   @param path: directory to change current working directory to
#   @rtype: boolean
#   @return: directory change succeeded
#   '''
#   return os.chdir(path)

# def getCurrentDirectory():
#   '''
#   Returns an absolute filename for the current directory.

#   @rtype: string
#   @return: path of current working directory
#   '''
#   return os.getcwd()

# def listDirectory(path):
#   '''
#   Adds an alphabetized list of the files in the specified directory
#   to the string vector list.  This list excludes the
#   names . and .. entries.

#   @type path: string
#   @param path: directory to list files in
#   @rtype: [string]
#   @return: alphabetized list of files in directory
#   '''
#   return os.listdir(path).sort()

# def getDirectoryPathSeparator():
#   '''
#   Returns the standard directory path separator used on this platform.

#   @rtype: string
#   '''
#   return os.sep

# def getSearchPathSeparator():
#   '''
#   Returns the standard search path separator used on this platform.

#   @rtype: string
#   '''
#   return os.pathsep

# def matchFilenamePattern(filename, pattern):
#   '''
#   Determines whether the filename matches the specified pattern.  The
#   pattern string is interpreted in much the same way that a Unix shell
#   expands filenames and supports the following wildcard options:

#       - ? Matches any single character
#       - * Matches any sequence of characters
#       - [...]  Matches any of the specified characters
#       - [^...] Matches any character except the specified ones

#   The last two options allow a range of characters to be specified in the
#   form a-z.

#   @type filename: string
#   @param filename: filename to check against pattern
#   @type pattern: string
#   @param pattern: pattern to verify
#   @rtype: boolean
#   '''
#   return recursiveMatch(filename, 0, pattern, 0)

# def splitPath(path):
#   '''
#   private method
#   '''
#   list = []
#   sep = ":" if (path.find(";") == -1) else ";"
#   path += sep
#   start = 0
#   while(True):
#       finish = path.find(sep, start)
#       if(finish == -1): break
#       if(finish > start + 1):
#           list.append(path[start:finish])
#       start = finish + 1

#   return list

# def recursiveMatch(str, sx, pattern, px):
#   '''
#   private method
#   '''
#   slen = len(str)
#   plen = len(pattern)
#   if(px == plen): return (sx == slen)
#   pch = pattern[px]

#   if(pch == "*"):
#       for i in range(sx, slen + 1):
#           if(recursiveMatch(str, i, pattern, px + 1)): return True
#       return False

#   if(sx == slen): return False

#   sch = str[sx]
#   if(pch == "["):
#       match = False
#       invert = False
#       px += 1
#       if(px == plen):
#           raise exception.StandardError # Throw error: missing ]
#           dummy = 1
#       if(pattern[px] == "^"):
#           px += 1
#           invert = True
#       while(px < plen and pattern[px] != "]"):
#           if(px + 2 < plen and pattern[px + 1] == "-"):
#               match = (match or (sch >= pattern[px] and sch <= pattern[px+2]))
#               px += 3
#           else:
#               match = (match or (sch == pattern[px]))
#               px += 1
#       if(px == plen):
#           raise exception.StandardError # throw error: missing ]
#           dummy = 1
#       if(match == invert): return False
#   elif(pch != "?"):
#       if(pch != sch): return False
#   return recursiveMatch(str, sx + 1, pattern, px +1)



# if __name__ == '__main__':
#     pass

