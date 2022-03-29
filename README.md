# ASH

### Installation:
Make sure to install python then:
```bash
git clone https://github.com/n30nyx/ash
cd ash && python3 main.py
```

### Coreutils:
There are a few pre-prepared coreutils, add them to the symlinks yourself if you wish to use them

### Usage:
There are several builtins into ASH


These include:
```
# for comments (not a builtin but a general purpose utility)
# most builtins start with `@` (except for exit and quit)
@bash echo hi
# or
@cmd echo hi
# each is adjusted accordingly for your os so you can run both without needing to change, pick which one is easist for you
@echo hi
# or
@print hi
# both are exactly the same again
@export myglobalvalue hello world
# this will set the global value of `myglobalvalue` to `hello world`
# or
@global myglobalvalue hello world
# You can use globals through the following:
%myglobalvalue%
# basically any line with the identifier will be set with the global value
# for configuring ash:
# @ashrc <key> <value>
# for example:
@ashrc startup echo ASH - Ashes dust to dust
#or for creating a symlink:
# @ashrc !add:symlinks <path>
# for example:
@ashrc !add:symlinks /home/runner/ash/test_bin
# remember, your symlinks CANNOT end with a `/`
# set a prefix instead of <path> ~ 
@ashrc prefix `~> `
#NOTE: you don't have to include the `, that was just to show the space
# Reset a value:
@ashrc !del:prefix
# You may also use @config as an alias of @ashrc
@reload
# reload the ash shell after making a change to the code
# set local variables:
$myvar = hello
# also use operations
$myvar += world

```

Executing scripts:
```
# for .bat or .sh files, it will be automated eg.
test
# if test.sh/bat is there, it will run
# if a file is in one of the symlinks, let's use `test_bin/` as an example
test.py
# test.py would run
# to run a specific local file, with no autocorrect, simply type:
#./<file>
#eg:
./todo.txt
```
### Exiting Ash:
```
# exit <status> (by default status will be `0`)
# quit is an alias of exit
# exit 9 (for a special status)
# or
exit
```

### Todo:
- Add .ash file support
- Package shell properly
- Add download coreutils
- Add `@pkg`
- @update