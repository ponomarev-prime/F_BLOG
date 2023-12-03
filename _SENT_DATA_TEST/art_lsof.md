# lsof

lsof is a command meaning "list open files", which is used in many Unix-like systems to report a list of all open files and the processes that opened them. 

[Удивительно полезный инструмент: lsof](https://habr.com/ru/companies/ruvds/articles/337934/)

```bash
lsof -a -i4 -i6 -i
```

```bash
sudo ls -lah /proc/98188/cwd
sudo ls -lah /proc/98188/fd
sudo ls -lah /proc/98188/root
sudo ls -lah /proc/98188/exe
```

[10 lsof (List of Open Files) Command Examples in Linux](https://www.tecmint.com/10-lsof-command-examples-in-linux/)

# Error `fuse.gvfsd-fuse file system`

```bash
$ sudo lsof -Pan -p 666
lsof: WARNING: can't stat() fuse.gvfsd-fuse file system /run/user/1001/gvfs
      Output information may be incomplete.
lsof: WARNING: can't stat() fuse.portal file system /run/user/1001/doc
      Output information may be incomplete.
```

[lsof: WARNING: can't stat() fuse.gvfsd-fuse file system /run/user/1000/gvfs Output information may be incomplete](https://askubuntu.com/questions/790273/lsof-warning-cant-stat-fuse-gvfsd-fuse-file-system-run-user-1000-gvfs-outp)