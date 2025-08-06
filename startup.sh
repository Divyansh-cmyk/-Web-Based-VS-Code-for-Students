#!/bin/bash

echo "Starting temporary code-server to install extensions..."

# Start code-server in the background (so extensions can be installed)
code-server --auth=none --port=8080 &

# Wait for it to fully start
sleep 15

# Install extensions
code-server --install-extension formulahendry.code-runner
code-server --install-extension ms-python.python
code-server --install-extension ms-vscode.cpptools
code-server --install-extension redhat.java
code-server --install-extension dbaeumer.vscode-eslint
code-server --install-extension ms-vscode.go
code-server --install-extension ms-dotnettools.csharp
code-server --install-extension esbenp.prettier-vscode
code-server --install-extension ritwickdey.liveserver

# Stop background code-server
pkill code-server

# Launch code-server normally
echo "Launching code-server normally..."
exec code-server --auth=none --port=8080
