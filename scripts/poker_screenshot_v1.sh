#!/usr/bin/env bash
set -euo pipefail

output_dir="$HOME/Desktop/poker_screenshots"
mkdir -p "$output_dir"

player_name=$(osascript <<'APPLESCRIPT'
tell application "System Events"
  activate
  set dialogText to text returned of (display dialog "Indtast spillerens navn til filnavn:" default answer "" buttons {"OK"} default button "OK")
end tell
return dialogText
APPLESCRIPT
)

if [[ -z "${player_name// }" ]]; then
  echo "Ingen navn angivet. Afbryder." >&2
  exit 1
fi

safe_name=$(echo "$player_name" | tr -cd '[:alnum:]_-')
if [[ -z "$safe_name" ]]; then
  echo "Navnet gav ingen gyldige tegn til filnavn." >&2
  exit 1
fi

timestamp=$(date +"%Y%m%d_%H%M%S")
output_path="$output_dir/${safe_name}_${timestamp}.png"

window_id=$(osascript <<'APPLESCRIPT'
tell application "System Events"
  set frontApp to first application process whose frontmost is true
  tell frontApp
    if (count of windows) is 0 then return ""
    return id of front window
  end tell
end tell
APPLESCRIPT
)

if [[ -z "$window_id" ]]; then
  echo "Kunne ikke finde det aktive vindue." >&2
  exit 1
fi

screencapture -l "$window_id" -x "$output_path"

echo "Gemte: $output_path"
