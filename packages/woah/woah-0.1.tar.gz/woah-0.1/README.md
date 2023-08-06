# Woah

Woah is a script that you can wrap commands with, and it will wait until the
load average is reasonable before running them.

# Usage

Similar to `nice`, you just start your command with `woah` and everything after
that will be run unchanged.

```
# Maybe you have a lot of shells doing stuff
woah tar -xvzf /tmp/foo.tar users/tim

# Limiting concurrency of xargs
(cd /users; ls -d *) | xargs -P32 -n1 --no-run-if-empty woah tar /tmp/{} /users/{}
```

# Bugs and such

https://github.com/thatch/woah

# License

Apache 2.0
