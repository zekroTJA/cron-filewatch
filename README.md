# cron-filewatcher

This is a little, dependency-less python script which tracks the status of files in a 
directory and executes the passed command on execution for each added, removed or changed 
file. This script is meant to be used in combination with a task scheduler like cron.

The script takes the following arguments:

```
usage: cron-filewatch.py [-h] --dir DIR [--recursive] [--ignoreinit] --command COMMAND

optional arguments:
  -h, --help            show this help message and exit
  --dir DIR, -d DIR     The directory to be watched for changes.
  --recursive, -r       Whether the directory is watched recursively or not.
  --ignoreinit          Whether to ignore initialization or not. If set to true, no 
                        action is taken on first run when no files were being tracked 
                        before. Otherwise, the handler will be called for   
                        each file in the directory.
  --command COMMAND, -c COMMAND
                        The command to be executed on file change.
```

This could be an example setup for this script using cron:

> `crontab -e`
```cron
*/30 * * * * python3 /home/user/cron-filewatch.py -d /home/user/myfiles -r --ignoreinit -c 'bash /home/user/myscript.sh'
```

The executed command is getting passed the following three arguments:

| Position | Type | Description | Example |
|----------|------|-------------|---------|
| `1` | `string` | The absolute path of the file. | `/home/user/myfiles/test.file` |
| `2` | `int` | The modification type.<br> - `1` → `CREATE`<br> - `2` → `REMOVE`<br> - `3` - `MOD` | `1`
| `3` | `string` | The JSON formatted file information blob. | `{"name": "test.file", "dir": "/home/user/myfiles/test.file", "modns": 1608985681661999800}`

---

© 2020 Ringo Hoffmann (zekro Development)  
Covered by the MIT License.