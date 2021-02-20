
1. API Service
    - Recieves HTTP requests made by twilio client
    - Scope
        - Handle responses back to twilio client (SMS)
        - Handle the downloading of `.torrent` files
        - Handles User Interaction

2. Torrent/FTP Client Service
    - Monitors Download Folder for new `.torrent` files
    - Limit downloads to 1 for bandwith/memory constraint
    - Remove Torrent File once download is started
    - Check every X minutes to see if downloaded finishes
    - Move finished file using FTP
    - Clean Data from Qbittorent client