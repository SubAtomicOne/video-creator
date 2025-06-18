#!/bin/bash



cd /root/video-creator-main || { echo "Directory not found"; exit 1; }
# Activate Python virtual environment
source venv/bin/activate


# Set log file
LOGFILE="/root/error/pipeline_$(date +'%Y%m%d_%H%M%S').log"

# Run your python script and catch errors
python main.py >> "$LOGFILE" 2>&1
python auto_uploader.py --noauth_local_webserver >> "$LOGFILE" 2>&1

if [ $? -eq 0 ]; then
    echo "Upload succeeded at $(date)" >> "$LOGFILE"
else
    echo "Upload failed at $(date)" >> "$LOGFILE"
fi
