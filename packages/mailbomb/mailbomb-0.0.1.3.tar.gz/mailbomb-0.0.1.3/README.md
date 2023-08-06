# mailbomb
## A python package to send corporate amounts of email quickly and easily

This python package (for Python 3.6) allows you to quickly send massive amounts of email to your customers.

## Installation

The package is available for install from `pip`:

    pip install mailbomb

And then you are good to go.

## Usage

Import the package in your Python script like so:

    import mailbomb.Mailbomb as mb

    nuke = mb.Mailbomb(host='smtp.example.com', port=465,
        login='user@example.com', key='vErYsEcReTpAsSkEy')
    nuke.load_target_list('targets.txt')        # Read targets line by line from a .txt-file
    nuke.remove_duplicate_targets()             # Removes duplicate targets
    nuke.add_target('target@targetdomain.com')  # Add a target manually
    nuke.add_header('From', 'Anonymous Attacker <anonymous@attacker.com>')
    nuke.add_header('Subject', 'You are being nuked. Enjoy!')
    nuke.add_header('Reply-To', 'Anonymous Attacker #2 <other@attacker.com>')
    nuke.load_html_message('message.html')
    nuke.starttls()
    nuke.launch_agents(50)
    nuke.terminate()

And the nuke will be launched. Details on adding target email addresses will follow soon as this functionality has not yet been implemented.

## Uninstallation

Uninstall the package using `pip`:

    pip uninstall mailbomb

Thank you for using this Python package!