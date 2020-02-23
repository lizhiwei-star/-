#unicodedata unicodedata.c    # static Unicode character database


# Modules with some UNIX dependencies -- on by default:
# (If you have a really backward UNIX, select and socket may not be
# supported...)

#fcntl fcntlmodule.c    # fcntl(2) and ioctl(2)
#spwd spwdmodule.c              # spwd(3)
#grp grpmodule.c                # grp(3)
#select selectmodule.c  # select(2); not on ancient System V

# Memory-mapped files (also works on Win32).
#mmap mmapmodule.c

# CSV file helper
#_csv _csv.c

# Socket module helper for socket(2)
_socket socketmodule.c

# Socket module helper for SSL support; you must comment out the other
# socket line above, and possibly edit the SSL variable:
# SSL=/usr/local/ssl
_ssl _ssl.c \
        -DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl \
        -L$(SSL)/lib -lssl -lcrypto

# The crypt module is now disabled by default because it breaks builds
# on many systems (where -lcrypt is needed), e.g. Linux (I believe).

#_crypt _cryptmodule.c # -lcrypt        # crypt(3); needs -lcrypt on some systems


# Some more UNIX dependent modules -- off by default, since these
# are not supported by all UNIX systems:

#nis nismodule.c -lnsl  # Sun yellow pages -- not everywhere
#termios termios.c      # Steen Lumholt's termios module
#resource resource.c    # Jeremy Hylton's rlimit interface

#_posixsubprocess _posixsubprocess.c  # POSIX subprocess module helper

# Multimedia modules -- off by default.
# These don't work for 64-bit platforms!!!
# #993173 says audioop works on 64-bit platforms, though.
# These represent audio samples or images as strings:

#audioop audioop.c      # Operations on audio samples


# Note that the _md5 and _sha modules are normally only built if the
# system does not have the OpenSSL libs containing an optimized version.

"Setup" 369L, 14487C                                                         214,2-9       59%
# system does not have the OpenSSL libs containing an optimized version.

# The _md5 module implements the RSA Data Security, Inc. MD5
# Message-Digest Algorithm, described in RFC 1321.

#_md5 md5module.c


# The _sha module implements the SHA checksum algorithms.
# (NIST's Secure Hash Algorithms.)
#_sha1 sha1module.c
#_sha256 sha256module.c
#_sha512 sha512module.c
#_sha3 _sha3/sha3module.c

# _blake module
#_blake2 _blake2/blake2module.c _blake2/blake2b_impl.c _blake2/blake2s_impl.c

# The _tkinter module.
#
# The command for _tkinter is long and site specific.  Please
# uncomment and/or edit those parts as indicated.  If you don't have a
# specific extension (e.g. Tix or BLT), leave the corresponding line
# commented out.  (Leave the trailing backslashes in!  If you
# experience strange errors, you may want to join all uncommented
# lines and remove the backslashes -- the backslash interpretation is
# done by the shell's "read" command and it may not be implemented on
# every system.

# *** Always uncomment this (leave the leading underscore in!):
# _tkinter _tkinter.c tkappinit.c -DWITH_APPINIT \
# *** Uncomment and edit to reflect where your Tcl/Tk libraries are:
#       -L/usr/local/lib \
# *** Uncomment and edit to reflect where your Tcl/Tk headers are:
#       -I/usr/local/include \
# *** Uncomment and edit to reflect where your X11 header files are:
#       -I/usr/X11R6/include \
# *** Or uncomment this for Solaris:
#       -I/usr/openwin/include \
# *** Uncomment and edit for Tix extension only:
#       -DWITH_TIX -ltix8.1.8.2 \
# *** Uncomment and edit for BLT extension only:
#       -DWITH_BLT -I/usr/local/blt/blt8.0-unoff/include -lBLT8.0 \
# *** Uncomment and edit for PIL (TkImaging) extension only:
#     (See http://www.pythonware.com/products/pil/ for more info)
#       -DWITH_PIL -I../Extensions/Imaging/libImaging  tkImaging.c \
# *** Uncomment and edit for TOGL extension only:
#       -DWITH_TOGL togl.c \
# *** Uncomment and edit to reflect your Tcl/Tk versions:
#       -ltk8.2 -ltcl8.2 \
# *** Uncomment and edit to reflect where your X11 libraries are:
#       -L/usr/X11R6/lib \
# *** Or uncomment this for Solaris:
#       -L/usr/openwin/lib \
# *** Uncomment these for TOGL extension only:
                                                                             240,1         76%
#       -L/usr/openwin/lib \
# *** Uncomment these for TOGL extension only:
#       -lGL -lGLU -lXext -lXmu \
# *** Uncomment for AIX:
#       -lld \
# *** Always uncomment this; X11 libraries to link with:
#       -lX11

# Lance Ellinghaus's syslog module
#syslog syslogmodule.c          # syslog daemon interface


# Curses support, requiring the System V version of curses, often
# provided by the ncurses library.  e.g. on Linux, link with -lncurses
# instead of -lcurses).

#_curses _cursesmodule.c -lcurses -ltermcap
# Wrapper for the panel library that's part of ncurses and SYSV curses.
#_curses_panel _curses_panel.c -lpanel -lncurses


# Modules that provide persistent dictionary-like semantics.  You will
# probably want to arrange for at least one of them to be available on
# your machine, though none are defined by default because of library
# dependencies.  The Python module dbm/__init__.py provides an
# implementation independent wrapper for these; dbm/dumb.py provides
# similar functionality (but slower of course) implemented in Python.

#_dbm _dbmmodule.c      # dbm(3) may require -lndbm or similar

# Anthony Baxter's gdbm module.  GNU dbm(3) will require -lgdbm:

#_gdbm _gdbmmodule.c -I/usr/local/include -L/usr/local/lib -lgdbm


# Helper module for various ascii-encoders
#binascii binascii.c

# Fred Drake's interface to the Python parser
#parser parsermodule.c


# Andrew Kuchling's zlib module.
# This require zlib 1.1.3 (or later).
# See http://www.gzip.org/zlib/
#zlib zlibmodule.c -I$(prefix)/include -L$(exec_prefix)/lib -lz

# Interface to the Expat XML parser
# More information on Expat can be found at www.libexpat.org.
#
#pyexpat expat/xmlparse.c expat/xmlrole.c expat/xmltok.c pyexpat.c -I$(srcdir)/Modules/expat -DHAVE_EXPAT_CONFIG_H -DUSE_PYEXPAT_CAPI

# Hye-Shik Chang's CJKCodecs

# multibytecodec is required for all the other CJK codec modules
#_multibytecodec cjkcodecs/multibytecodec.c

#_codecs_cn cjkcodecs/_codecs_cn.c
#_codecs_hk cjkcodecs/_codecs_hk.c
#_codecs_iso2022 cjkcodecs/_codecs_iso2022.c
#_codecs_jp cjkcodecs/_codecs_jp.c
#_codecs_kr cjkcodecs/_codecs_kr.c
#_codecs_tw cjkcodecs/_codecs_tw.c

# Example -- included for reference only:
# xx xxmodule.c

# Another example -- the 'xxsubtype' module shows C-level subtyping in action
xxsubtype xxsubtype.c

# Uncommenting the following line tells makesetup that all following modules
# are not built (see above for more detail).
#
#*disabled*
#
#_sqlite3 _tkinter _curses pyexpat
#_codecs_jp _codecs_kr _codecs_tw unicodedata