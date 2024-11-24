#!/bin/bash

# Check if sufficient arguments are passed
if [ $# -lt 2 ]; then
    echo "Usage: $0 <host> <port>"
    exit 1
fi

# Input Arguments
host=$1
port=$2

# Function to test TCP connection with a timeout of 300ms
test_connection() {
    local host=$1
    local port=$2
    nc -z -w 3.3 $host $port &>/dev/null
    return $?
}

# Retry count
RETRY_LIMIT=3
RETRY_COUNT=0

# Wait for TCP Connection to be ready
echo "Waiting for connection at $host:$port..."
while ! test_connection $host $port; do
    ((RETRY_COUNT++))
    if [ $RETRY_COUNT -ge $RETRY_LIMIT ]; then
        echo "Failed to connect to $host:$port after $RETRY_LIMIT attempts."
        exit 1
    fi
    echo "Service at $host:$port not yet available, retrying ($RETRY_COUNT/$RETRY_LIMIT)..."
    sleep 5
done
echo "Connection to $host:$port successful."

echo "The service at $host:$port is reachable. Starting the application..."
# Replace the following with the command to start your application
# ./your-application-start-command
