from fabric import Connection

def deploy():
    # Connect to the remote server
    c = Connection('your_server_ip')

    # Pull the latest changes from your Git repository
    c.run('cd /path/to/your/repository && git pull')

    # Install dependencies
    c.run('cd /path/to/your/repository && pip install -r requirements.txt')

    # Restart the web server
    c.sudo('systemctl restart apache2')  # Replace with your web server command

    # Print a success message
    print('Website deployed successfully!')

# Run the deploy function
deploy()