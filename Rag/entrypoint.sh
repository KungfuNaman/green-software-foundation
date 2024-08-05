#!/bin/bash
set -e

# Start systemd
exec /lib/systemd/systemd

## Start systemd in the background
#/usr/sbin/init &
#
## Give systemd some time to start
#sleep 5

# Start the backend script
/start_backend.sh

# Keep the container running
tail -f /dev/null