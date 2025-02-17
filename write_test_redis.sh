if ! command -v redis-server &> /dev/null; then
    echo "Redis not installed. Installing... "
    if ! command -v sudo &> /dev/null; then
        echo "ERROR: sudo is needed"
        exit 1
    fi
    
    sudo apt update
    sudo apt install -y redis-server
    
    if ! command -v redis-server &> /dev/null; then
        echo "ERROR: Installation fail!"
        exit 1
    fi
    echo "Installation Success!"
else
    echo "Redis has been installed!"
fi

if ! pgrep redis-server > /dev/null; then
    echo "Start Redis..."
    sudo systemctl start redis-server
    sleep 2 
fi

if ! redis-cli ping > /dev/null 2>&1; then
    echo "ERROR: Redis Server fails to start!"
    exit 1
fi

echo "Start testing..."
redis-benchmark -t set -n 100000 -d 1024
echo "Success!"