PIDS=$(netstat -ano | grep ':3000' | awk '{print $5}') 
if [ -n "$PIDS" ]; then for PID in $PIDS; do 
    echo "Killing process with PID $PID using port 3000" 
    taskkill //F //PID $PID done fi

cd frontend
pnpm dev &
sleep 3
cd ..
python main.py