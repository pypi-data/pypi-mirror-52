# NAME

xpylog - an xconsole-like syslog monitor on X11

![screenshot](https://raw.githubusercontent.com/h-ohsaki/xpylog/master/screenshot/xpylog.gif)

# SYNOPSIS

xpylog

# DESCRIPTION

This manual page documents **xpylog**, a realtime syslog monitor on X Window
System.  **xpylog** is a xconsole-like simple monotoring application with
several additional features.

# OPTIONS

None

# REQUIREMENTS

**xpylog** obtains the syslog messages via `journalctl` command in systemd.

# INSTALLATION

```sh
$ pip3 install xpylog
```

# AVAILABILITY

The latest version of **xpylog** is available at PyPI
(https://pypi.org/project/xpylog/) .

# SEE ALSO

xpywm(1), xconsole(1), journalctl(1), systemd(1)

# AUTHOR

Hiroyuki Ohsaki <ohsaki[atmark]lsnl.jp>
