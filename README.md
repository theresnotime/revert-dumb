# revert-dumb
Run a potentially dumb command and revert it if it "fails" (_i.e. you can't cancel the timeout with Ctrl-C because you've just blocked SSH and been disconnected_)

# Usage example
This would run `sudo ufw enable`, wait 2 minutes, and then run `sudo ufw disable` if not cancelled with `Ctrl-C` (thus proving the user hasn't been locked out or something...)

```bash
revert-dumb --time 120 --action 'sudo ufw enable' --recovery 'sudo ufw disable'
```

# Options
```
-t, --time: amount of time in seconds to wait before running recovery commands. (10 - 3600, default 120)
-a, --action: the potentially dumb commands to run
-r, --recovery: the recovery commands to run
-h, --help: Show this help text
-v, --version: Show version information
```

# Tips
- You can always invoke a script (for either `--action` or `--recovery`) for complex commands — e.g. `--recovery 'bash /path/to/script.sh'`


## Alias
You can use the binaries in the release, but tbh I'd just run the python script directly seeing as it doesn't depend on anything non-standard (afaik) — I'm sure someone will say this is a bad idea, but I just added this to my `.bashrc`

```bash
alias revert-dumb='python3 ~/revert-dumb/revert-dumb.py'
```

# A note for me
## Building
 - `python -m nuitka --standalone --onefile --output-dir=out .\revert-dumb.py`