from setup_db import execute_query

role = execute_query("SELECT role_id FROM user WHERE user_email='admin@admin.com' and user_password='admin'")[0][0]
print(role)
