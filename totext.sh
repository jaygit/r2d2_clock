#!/bin/bash

echo "Processing..."
wget -q -U "Mozilla/5.0" --post-file stt.flac --header "Content-Type: audio/x-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=en-us&client=chromium&key=AIzaSyCnl6MRydhw_5fLXIdASxkLJzcJh5iX0M4" | cut -d\" -f12  > stt.txt
#wget -q -U "Mozilla/5.0" -post-file stt.flac -header "Content-Type: audio/x-flac; rate=16000" -O -- "http://www.google.com/speech-api/v1/recognize?lang=en-us&client=chromium" | cut -d\" -f12 > stt.txt

echo -n "You Said: "
cat stt.txt

rm stt.flac > /dev/null 2>&1
