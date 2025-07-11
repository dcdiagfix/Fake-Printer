from flask import Flask, render_template, request, redirect, url_for, flash
from ldap3 import Server, Connection, ALL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Admin credentials
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials. Please try again.'
    return render_template('login.html', username='admin', password='password')

# Route for the dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        server_ip = request.form['serverIP']
        try:
            # Connect to the LDAP server with the specified IP and credentials
            server = Server(f'ldap://{server_ip}', port=389, get_info=ALL)
            conn = Connection(server, user=username, password=password)
            
            if conn.bind():
                result = f'Successfully connected to {server_ip} on port 389 with username {username}'
            else:
                result = f'Failed to connect to {server_ip} on port 389 with username {username}'
            
            conn.unbind()
        except Exception as e:
            # In case of an error, return to the dashboard and flash an error message
            flash(f'Error: Unable to connect to {server_ip} on port 389. Please check the details and try again.', 'error')
            return redirect(url_for('dashboard'))
        
        # Return result as a message on success or failure
        flash(result, 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('dashboard.html', username='ad.vuln.local\\svc-scanning', password='Sc@nn1ng', serverIP='')

if __name__ == '__main__':
    app.run(debug=True)
