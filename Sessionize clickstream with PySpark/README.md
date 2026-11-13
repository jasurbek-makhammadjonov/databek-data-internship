Clickstream Sessionization with PySpark
Problem
Given clickstream events (user_id, ts, url):

Assign session IDs
Start a new session after 30 minutes of inactivity
Compute sessions per day
Compute average session length
Run
pip install -r requirements.txt
spark-submit sessionization.py