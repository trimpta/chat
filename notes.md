# chat v3

## should be able to

- run purely on stdlib
- chat
- switch modes bw input and chat
- send small text files.
- have admin users
- send dm
- work over ngrok ( use only one port :)
- proper exit handling
- suck less

## arch

well the client has to be able to switch contexts, so it has to keep a list of messages.

there has to be a way to send over files, and since i plan on using json, i can just do it via json...

the types of messages are probably

- global messages
- dms
- text embeds
- system messages

for the file sharing, i plan to have a download on demand model, so whenever someone uploads a file, it gets stored on the server. users can run a command to see stored files, and download any one that they like

should use select with stdin.readline() to preserve user input and show messages realtime

commands i wanna include are

- /exit
- /help
- /list
- /whisper or /dm
- /upload
- /listfiles
- /download

admin commands

- /kick
- /deletefile
- /tellrawnb

some server side features i wanna include this time are

- proper logging of messages and events

i think i'll go with plain text encoded messages bw server and clients. something like `MSGHello Guys!!` and `CMDWHISP user1,user2 i think user3 is crazy!`

how should i implement commands?
