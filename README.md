# NightChord

### Python-Based music creation software, capable of converting a lyric video on Youtube into a [video like this](https://www.youtube.com/watch?v=ZbNzXQX542c)

## Introduction

I used this project as an introduction to Python Classes and to stregnthen my REGEX skills.

This program can generate Nightcore video by inputting one of the following paramters:

 * Youtube URL
 * Artist / Song Name
 * Locally Saved MP4/AVI
 * Locally Saved MP3

You can also pull song names from Billboard Top-X Charts to use for video generation.

Essentially, this programs automates the process of Downloading/Remixing/Transcribing/Uploading Nightcore videos.  I have automated all of these processes using various techniques.  Everything I'm currently using is more of a proof of concept solution rather than a solution that's set to scale.

## Song List (Audio Only)

- [Nightcore - DNA](https://soundcloud.com/user-367430385/nightcore-dna)

- [Nightcore - Broken Heart](https://soundcloud.com/user-367430385/nightcore-broken-heart)

- [Nightcore - Psychopath](https://soundcloud.com/user-367430385/nightcore-psychopath)

- [Nightcore - Empty Picture Frames](https://soundcloud.com/user-367430385/nightcore-empty-picture-frames)

- [Nightcore - Come Home](https://soundcloud.com/user-367430385/nightcore-come-home)

- [Nightcore - Anxiety](https://soundcloud.com/user-367430385/nightcore-anxiety)

- [Nightcore - Arizona](https://soundcloud.com/user-367430385/nightcore-arizona)

- [Nightcore - London](https://soundcloud.com/user-367430385/nightcore-london-1)

- [Nightcore - Give Me a Try](https://soundcloud.com/user-367430385/nightcore-give-me-a-try)





Current Features:

* Create Video with Youtube URL
* Create Video with Youtube Artist / Song
* Create both MP3 and MP4 Files
* Generate Videos from Top-X Billboard Chart Songs
* Recreate Lyric Videos with ~98% Accuracy
* Randomly Choose Background Images from a database of Anime Wallpapers
* Cycle through User-Agents to reduce Requests Limits on Youtube
* Set song speed and pitch change
* Grab words with low OCR Confidence
* Send unknown words to [DeathByCaptcha](http://www.deathbycaptcha.com/) to obtain 100% Accuracy
* Generate Word Coordinates in Lyric Videos
* Calculate Amount of Spaces in a lyric video (To Improve Accuracy of OCR)
* Write OCR results to an image with dynamic font choice

