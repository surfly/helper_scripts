Add agents in batch by running this python2 script: python add_surfly_agents.py

You will be asked to provide a valid REST API key.

If your key is valid you will be prompted to provide the path to a CSV input file.

Each row in your input CSV should contain nothing more than: agent_name, agent_email, password
(The script will iterate over every row, so its suggested not to include a "headers" row - see example.csv).

Running this script also generates a report in the form of a CSV file. This will be saved as 'surfly_agents_added_report.csv', and shows wether or not each addition was successful (will contain an agent_id for all new agents).
