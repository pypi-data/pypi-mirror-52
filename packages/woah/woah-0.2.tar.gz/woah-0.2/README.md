# Woah

Woah is a script that you can wrap commands with, and it will wait until the
load average is reasonable before running them.

# Usage

Similar to `nice`, you just start your command with `woah` and everything after
that will be run unchanged.

Say, if you have a lot of other things going on, and want your backup to wait
for things to settle down...

```
woah tar -xvzf /tmp/foo.tar users/tim
```

Or you're running multiple things with xargs, but some are more expensive than
others and you want to keep your machine somewhat responsive...

```
(cd /users; ls -d *) | xargs -P32 -n1 --no-run-if-empty woah tar /tmp/{} /users/{}
```

# Bugs and such

https://github.com/thatch/woah

# License

Apache 2.0
