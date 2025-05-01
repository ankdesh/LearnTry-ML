#!/bin/bash

# Create the root directory structure and files
echo "Creating root directory files..."
touch README.md
touch requirements.txt
touch.env.example
touch.env # Note:.env is typically gitignored
touch run_server.py
touch run_client.py

# Create the a2a_interface directory and its contents
echo "Creating a2a_interface directory..."
mkdir -p a2a_interface
touch a2a_interface/__init__.py
touch a2a_interface/server.py
touch a2a_interface/handlers.py
touch a2a_interface/schemas.py
touch a2a_interface/agent_card.json

# Create the adk_core directory and its contents
echo "Creating adk_core directory..."
mkdir -p adk_core
touch adk_core/__init__.py
touch adk_core/agent.py
touch adk_core/tools.py
touch adk_core/memory.py

# Create the decoupling_interface directory and its contents
echo "Creating decoupling_interface directory..."
mkdir -p decoupling_interface
touch decoupling_interface/__init__.py
touch decoupling_interface/interface.py
touch decoupling_interface/implementation.py

# Create the client directory and its contents
echo "Creating client directory..."
mkdir -p client
touch client/__init__.py
touch client/a2a_client.py
touch client/cli.py

# Create the shared directory and its contents
echo "Creating shared directory..."
mkdir -p shared
touch shared/__init__.py
touch shared/models.py
touch shared/config.py

# Create the tests directory and its subdirectories/contents
echo "Creating tests directory..."
mkdir -p tests/test_a2a_interface
mkdir -p tests/test_adk_core
mkdir -p tests/test_decoupling_interface
mkdir -p tests/test_e2e

touch tests/__init__.py
touch tests/test_a2a_interface/__init__.py
touch tests/test_adk_core/__init__.py
touch tests/test_decoupling_interface/__init__.py
touch tests/test_e2e/__init__.py

echo "Directory structure created successfully."

# Optional: Display the created structure using tree (if installed)
if command -v tree &> /dev/null
then
    echo "Generated structure:"
    tree.
else
    echo "Install 'tree' to visualize the directory structure."
fi

exit 0