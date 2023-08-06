# update-plex-music-album-covers

Is your Plex showing waveforms or label covers instead of the posters (covers) you worked or paid for?

Update Plex music album covers to the corresponding front covers embedded in your MP3 files.

## Rationale

This utility was written as a solution to a problem with Plex Media Server and music album covers.
Some MP3 files such as the ones purchased from Beatport come with the usual cover one would expect
as well as an additional waveform image. They often include a label cover too.
When scanning files for covers Plex Media Server sees all of these and selects one seemingly
at random. This utility scans your music library for albums with multiple covers, attempts
to extract the embedded front covers from the MP3 files themselves and updates the album
covers with the those. The MP3 files are not modified in this process.

## Running

Install via PIP and run

```bash
python3 -m pip install update-plex-music-album-covers
update-plex-music-album-covers USERNAME --password PASSWORD SERVER LIBRARY
```
