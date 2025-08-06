# Use official code-server image
FROM codercom/code-server:latest

# Switch to root to install packages
USER root

# Install required packages
RUN mkdir -p /var/lib/apt/lists/partial && \
    chmod -R 755 /var/lib/apt/lists && \
    apt-get update && apt-get install -y \
    python3 \
    openjdk-17-jdk \
    gcc \
    g++ \
    curl \
    git && \
    rm -rf /var/lib/apt/lists/*

# Create Python symlink
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Copy startup script
COPY startup.sh /usr/bin/startup.sh
RUN chmod +x /usr/bin/startup.sh

# Switch back to non-root user
USER coder

# Set entrypoint
CMD ["/usr/bin/startup.sh"]
