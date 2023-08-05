# Utility python script

Mix of utility python scripts.

## Install
`pip3 install utility-python-script`

## Script

### pulseaudio_switch

#### Description
Change the default audio device and move all active streams to the new audio device in
pulseaudio.
Check in `pacmd list` the index number of the audio source device or find out the corresponding
index number of your soundcard by trying out the index numbers, starting from 0; i in ℕ.

#### Example
`pulseaudio_switch --output_sink 1`

### rsync-python

#### Description
Rsync files specified in a `JSON` config. If a mountpoint is specified, then only `rsync` if the
mountpoint is mounted.

#### Config example
`/etc/utilpys/rsync-python-script.json`
```
{
  "3tb-to-4tb": {
    "src": "/mnt/3tb/file",
    "dst": "/mnt/4tb01/file",
    "mp": ["/mnt/3tb", "/mnt/4tb01"]
  },
  "user-dev-to-4tb": {
    "src": "/home/user/dev",
    "dst": "/mnt/3tb/dev",
    "mp": ["/mnt/3tb", "/"]
  }
}
```

#### Run
`rsync_python_script`
