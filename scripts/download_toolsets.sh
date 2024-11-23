#!/bin/bash
# scripts/download_toolsets.sh

# Read toolsets config
while IFS= read -r line
do
  if [[ $line =~ repo:\ \"(.*)\" ]]; then
    REPO="${BASH_REMATCH[1]}"
    # Clone repo to appropriate tools directory
    git clone $REPO /app/external_tools/
  fi
done < /app/config/toolsets.yml

# Execute passed command (usually starting the server)
exec "$@"
