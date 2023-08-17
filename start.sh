#!/bin/bash
cd ../odoo # Navigate to directory
python3 odoo-bin --addons-path=./addons,../enterprise -d test_db & # Start the server
sleep 5 # Wait for the server to start
open http://localhost:8069 # Open the browser
