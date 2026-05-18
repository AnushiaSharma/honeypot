import sqlite3

from flask import (
    Flask,
    request,
    render_template,
    redirect,
    session,
    make_response
)

from database import (
    insert_attack,
    init_db,
    get_location
)

from datetime import (
    timedelta,
    datetime
)

app = Flask(__name__)

# SESSION SECURITY

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

app.secret_key = 'supersecretkey'

app.permanent_session_lifetime = timedelta(
    minutes=5
)

# INITIALIZE DATABASE

init_db()

# FAKE LOGIN PAGE

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        username = request.form.get('username')

        password = request.form.get('password')

        ip = request.remote_addr

        # TRACK ATTEMPTS

        attempts = session.get('attempts', 0)

        attempts += 1

        session['attempts'] = attempts

        # CURRENT TIME

        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # LOCATION

        country, city, latitude, longitude = get_location(ip)

        # STORE ATTACK

        insert_attack(
            ip,
            username,
            password,
            country,
            city,
            latitude,
            longitude,
            current_time
        )

        # ATTEMPT LOGIC

        if attempts >= 3:

            return render_template(
                'login.html',
                error="""
                Account temporarily locked.
                Please contact administrator.
                """,
                locked=True
            )

        remaining = 3 - attempts

        return render_template(
            'login.html',
            error=f"""
            Incorrect credentials.
            {remaining} attempt(s) remaining.
            """
        )

    # RESET SESSION ON FRESH VISIT

    session['attempts'] = 0

    return render_template(
        'login.html'
    )

# ADMIN LOGIN

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':

        username = request.form.get(
            'username'
        )

        password = request.form.get(
            'password'
        )

        if (
            username == "admin"
            and
            password == "admin123"
        ):

            session.permanent = True

            session['admin'] = True

            return redirect('/dashboard')

        else:

            return "Access Denied"

    return render_template(
        'admin_login.html'
    )

# DASHBOARD

@app.route('/dashboard')
def dashboard():

    if not session.get('admin'):

        return redirect('/admin')

    conn = sqlite3.connect(
        'database.db'
    )

    cursor = conn.cursor()

    # ATTACKS

    cursor.execute(
        "SELECT * FROM attacks"
    )

    rows = cursor.fetchall()

    # COMMANDS

    cursor.execute(
        """
        SELECT * FROM commands
        ORDER BY id DESC
        LIMIT 10
        """
    )

    commands = cursor.fetchall()

    # TOTAL ATTACKS

    cursor.execute(
        "SELECT COUNT(*) FROM attacks"
    )

    total = cursor.fetchone()[0]

    conn.close()

    response = make_response(

        render_template(
            'dashboard.html',
            data=rows,
            commands=commands,
            total=total
        )

    )

    # CACHE PROTECTION

    response.headers[
        'Cache-Control'
    ] = 'no-store, no-cache, must-revalidate, max-age=0'

    response.headers[
        'Pragma'
    ] = 'no-cache'

    response.headers[
        'Expires'
    ] = '0'

    return response

# LOGOUT

@app.route('/logout')
def logout():

    session.pop('admin', None)

    return redirect('/admin')

# START SERVER

def start_web():

    app.run(
        host='0.0.0.0',
        port=8080
    )