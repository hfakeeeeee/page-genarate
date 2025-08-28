#!/bin/bash

folder="$1"
port="$2"
allowedHosts="$3"

cd ./projects || exit

unzip $folder.zip -d $folder

cd "$folder" || exit

if [[ -f "vite.config.ts" ]]; then
  FILE="vite.config.ts"
elif [[ -f "vite.config.js" ]]; then
  FILE="vite.config.js"
else
  exit 1
fi

ALLOWED_ARRAY=$(echo "$allowedHosts" | awk -F, '{for(i=1;i<=NF;i++) printf "            \"%s\"%s\\n", $i, (i<NF?",":"") }')

SERVER_CONFIG=$(cat <<EOF
server: {
        host: "0.0.0.0",
        port: $port,
        strictPort: true,
        allowedHosts: [
$ALLOWED_ARRAY        ]
    }
EOF
)

TMP_FILE=$(mktemp)

awk -v replacement="$SERVER_CONFIG" '
{
    if ($0 ~ /update_me/) {
        print replacement
    } else {
        print $0
    }
}' "$FILE" > "$TMP_FILE"

mv "$TMP_FILE" "$FILE"

npm install
npm run dev -- --port $port &

disown