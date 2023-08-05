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

**xpylog** obtains the syslog messges via the named pipe `/dev/xconsole`.
Thus, the named pipe (FIFO (First-In First-Out)) `/dev/xconsole` must exist in
`/dev` directory, and it must be readable by the user running **xpylog**
program.

For instance, `/etc/syslog.conf` or `/etc/rsyslog.conf` must have been
configured to send messages to `/dev/xconsole` as
```
daemon.*;mail.*;\
	news.err;\
	*.=debug;*.=info;\
	*.=notice;*.=warn	|/dev/xconsole
```

If `/dev/xconsole` does not exist, you can create the named pipe by
```sh
$ sudo mkfifo /dev/xconsole
```

Also, make sure `/dev/xconsole` is readable:
```
$ ls -al /dev/xconsole 
prw-r----- 1 root adm 0 Jul  5 23:34 /dev/xconsole|
$ id
uid=1000(ohsaki) ...,4(adm),...
```

# INSTALLATION

```sh
$ pip3 install xpylog
```

# AVAILABILITY

The latest version of **ansiterm** module is available at PyPI
(https://pypi.org/project/xpylog/) .

# SEE ALSO

xpywm(1), xconsole(1), rsyslog.conf(8)

# AUTHOR

Hiroyuki Ohsaki <ohsaki[atmark]lsnl.jp>
