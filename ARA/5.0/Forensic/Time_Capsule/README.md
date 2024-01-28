# Time Capsule

**Category** : Forensic
**Points** : 245

I discovered my old time capsule and it has my favorite song in it. The problem is, I forgot the password, and due to its age, the file inside might be corrupted. I also found the note that I wrote a long time ago about the password. My cat said that you might be able to help me. Can you?.

Attachment : [time](https://drive.google.com/file/d/1DPG8-DXF64JXOAZczyGiHeX_clY7yU_a/view?usp=sharing),[note](https://drive.google.com/file/d/1F8KhEB_CE9U1KHy2OpR4wGTmUOQfp5pC/view?usp=sharing).
Author: zalv

## SOlve

Diberikan sebuah 2 file notes.png dan sebuah .zip file, notes .png berisi clue dari bruteforce pw yang berisi
`future me, these are 6 elements for the password ;)

1. My month of birth (in number)
2. One of my favorite character : kAor1, s3nKu, sTev3, Lev1, L1Ly
   23456 3. 4.
   One random character of: {'\*', '#', '!', '%', '&', '+'}
   My favorite number (from 0 to 9)
3. One random letter between A to Z
4. One random character of : {'\*', '#', '!', '%', '&', '+'}
   If you still can't recall the format, here's an example: 5kAor1%3U+`

Namun zip tersebut ternyata corrupted
`❯ unzip TimeCapsule.zip
Archive:  TimeCapsule.zip
   skipping: MyCapsule.zip           supported compression method 99`
Mari kita edit hex nya yang awalnya `Compression Method    0063 'AES Encryption'` Menjadi `Compression Method  0008 'Deflated'`

Dan boom sudah ter repair. mari kita bruteforce :). solver ada di solver.py

`Unsolved`
