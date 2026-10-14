# ============================================================
# SpectrumSim - Intelligent Spectrum Allocation Simulator
# File: App.py
# ============================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import sqlite3
import os


# ============================================================
# IMPORT ALGORITHMS
# ============================================================

from algorithms.first_fit import perform_first_fit
from algorithms.best_fit import perform_best_fit
from algorithms.interference import check_interference


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

app.secret_key = "spectrumsim_secret_key_2026"


# ============================================================
# DATABASE
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE = os.path.join(
    BASE_DIR,
    "database.db"
)


def get_db_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allocations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user TEXT NOT NULL,

            service_type TEXT NOT NULL,

            start_frequency REAL NOT NULL,

            bandwidth REAL NOT NULL,

            end_frequency REAL NOT NULL,

            algorithm TEXT NOT NULL,

            status TEXT DEFAULT 'Active',

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


# Create database/table when application starts
initialize_database()


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        # Demo login
        if (
            username == "admin"
            and
            password == "admin123"
        ):

            session["logged_in"] = True

            session["username"] = username

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid username or password.",
            "error"
        )

        return render_template(
            "login.html"
        )

    return render_template(
        "login.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# LOGIN CHECK
# ============================================================

def is_logged_in():

    return session.get(
        "logged_in",
        False
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    connection = get_db_connection()

    allocations = connection.execute(
        """
        SELECT *
        FROM allocations
        ORDER BY id DESC
        LIMIT 5
        """
    ).fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        allocations=allocations
    )


# ============================================================
# SPECTRUM
# ============================================================

@app.route("/spectrum")
def spectrum():

    connection = get_db_connection()

    allocations = connection.execute(
        """
        SELECT *
        FROM allocations
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "spectrum.html",
        allocations=allocations
    )


# ============================================================
# ALLOCATION
# ============================================================

@app.route(
    "/allocation",
    methods=["GET", "POST"]
)
def allocation():

    if request.method == "POST":

        try:

            # ------------------------------------------------
            # GET FORM VALUES
            # ------------------------------------------------

            user = request.form.get(
                "user",
                ""
            ).strip()

            service_type = request.form.get(
                "type",
                ""
            ).strip()

            frequency = float(
                request.form.get(
                    "frequency",
                    0
                )
            )

            bandwidth = float(
                request.form.get(
                    "bandwidth",
                    0
                )
            )

            algorithm = request.form.get(
                "algorithm",
                "first_fit"
            )


            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if user == "":

                flash(
                    "Please enter User / Service Name.",
                    "error"
                )

                return render_template(
                    "allocation.html"
                )


            if service_type == "":

                flash(
                    "Please select Service Type.",
                    "error"
                )

                return render_template(
                    "allocation.html"
                )


            if bandwidth <= 0:

                flash(
                    "Bandwidth must be greater than 0.",
                    "error"
                )

                return render_template(
                    "allocation.html"
                )


            if frequency < 700:

                flash(
                    "Frequency cannot be below 700 MHz.",
                    "error"
                )

                return render_template(
                    "allocation.html"
                )


            if frequency > 950:

                flash(
                    "Frequency cannot exceed 950 MHz.",
                    "error"
                )

                return render_template(
                    "allocation.html"
                )


            requested_end = (
                frequency +
                bandwidth
            )


            if requested_end > 950:

                flash(
                    "Frequency range cannot exceed 950 MHz.",
                    "error"
                )

                return render_template(
                    "allocation.html"
                )


            # ------------------------------------------------
            # AVAILABLE SPECTRUM
            # ------------------------------------------------

            available_bands = [
                (700, 750),
                (750, 800),
                (800, 850),
                (850, 900),
                (900, 950)
            ]


            # ------------------------------------------------
            # SELECT ALLOCATION ALGORITHM
            # ------------------------------------------------

            if algorithm == "best_fit":

                result = perform_best_fit(
                    available_bands,
                    bandwidth
                )

            else:

                algorithm = "first_fit"

                result = perform_first_fit(
                    available_bands,
                    bandwidth
                )


            # ------------------------------------------------
            # CHECK ALLOCATION RESULT
            # ------------------------------------------------

            if not result["success"]:

                flash(
                    "No suitable spectrum available.",
                    "error"
                )

                return render_template(
                    "allocation.html"
                )


            allocated_start = (
                result["allocation"][0]
            )

            allocated_end = (
                result["allocation"][1]
            )


            # ------------------------------------------------
            # SAVE ALLOCATION TO DATABASE
            # ------------------------------------------------

            connection = get_db_connection()

            connection.execute(
                """
                INSERT INTO allocations
                (
                    user,
                    service_type,
                    start_frequency,
                    bandwidth,
                    end_frequency,
                    algorithm,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user,
                    service_type,
                    allocated_start,
                    bandwidth,
                    allocated_end,
                    algorithm,
                    "Active"
                )
            )

            connection.commit()

            connection.close()


            # ------------------------------------------------
            # RESULT PAGE
            # ------------------------------------------------

            return render_template(
                "result.html",

                user=user,

                service_type=service_type,

                frequency=allocated_start,

                bandwidth=bandwidth,

                end_frequency=allocated_end,

                algorithm=algorithm,

                status="Active"
            )


        except ValueError:

            flash(
                "Please enter valid numeric values.",
                "error"
            )

            return render_template(
                "allocation.html"
            )


        except Exception as error:

            print(
                "Allocation Error:",
                error
            )

            flash(
                "An error occurred during allocation.",
                "error"
            )

            return render_template(
                "allocation.html"
            )


    # ------------------------------------------------
    # GET REQUEST
    # ------------------------------------------------

    return render_template(
        "allocation.html"
    )


# ============================================================
# INTERFERENCE
# ============================================================

@app.route(
    "/interference",
    methods=["GET", "POST"]
)
def interference():

    result = None

    if request.method == "POST":

        try:

            start1 = float(
                request.form.get(
                    "start1",
                    0
                )
            )

            bandwidth1 = float(
                request.form.get(
                    "bandwidth1",
                    0
                )
            )

            start2 = float(
                request.form.get(
                    "start2",
                    0
                )
            )

            bandwidth2 = float(
                request.form.get(
                    "bandwidth2",
                    0
                )
            )


            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------

            if (
                bandwidth1 <= 0
                or
                bandwidth2 <= 0
            ):

                flash(
                    "Bandwidth must be greater than zero.",
                    "error"
                )

                return render_template(
                    "interference.html",
                    result=None
                )


            # ------------------------------------------------
            # RUN INTERFERENCE ALGORITHM
            # ------------------------------------------------

            result = check_interference(

                start1,
                bandwidth1,

                start2,
                bandwidth2
            )


            # ------------------------------------------------
            # ADD FREQUENCY INFORMATION
            # ------------------------------------------------

            result["start1"] = start1

            result["end1"] = (
                start1 +
                bandwidth1
            )

            result["start2"] = start2

            result["end2"] = (
                start2 +
                bandwidth2
            )


        except ValueError:

            flash(
                "Please enter valid numeric values.",
                "error"
            )


        except Exception as error:

            print(
                "Interference Error:",
                error
            )

            flash(
                "An error occurred while checking interference.",
                "error"
            )


    return render_template(
        "interference.html",
        result=result
    )


# ============================================================
# SIMULATION
# ============================================================

@app.route(
    "/simulation",
    methods=["GET", "POST"]
)
def simulation():

    simulation_result = None

    if request.method == "POST":

        try:

            bandwidth = float(
                request.form.get(
                    "bandwidth",
                    20
                )
            )


            # ------------------------------------------------
            # AVAILABLE SPECTRUM
            # ------------------------------------------------

            available_bands = [
                (700, 750),
                (750, 800),
                (800, 850),
                (850, 900),
                (900, 950)
            ]


            # ------------------------------------------------
            # FIRST FIT
            # ------------------------------------------------

            first_fit_result = perform_first_fit(
                available_bands,
                bandwidth
            )


            # ------------------------------------------------
            # BEST FIT
            # ------------------------------------------------

            best_fit_result = perform_best_fit(
                available_bands,
                bandwidth
            )


            # ------------------------------------------------
            # SIMULATION RESULT
            # ------------------------------------------------

            simulation_result = {

                "bandwidth": bandwidth,

                "first_fit":
                    first_fit_result,

                "best_fit":
                    best_fit_result

            }


        except ValueError:

            flash(
                "Please enter a valid bandwidth.",
                "error"
            )


        except Exception as error:

            print(
                "Simulation Error:",
                error
            )

            flash(
                "An error occurred during simulation.",
                "error"
            )


    return render_template(
        "simulation.html",
        simulation_result=simulation_result
    )


# ============================================================
# REPORTS
# ============================================================

@app.route("/reports")
def reports():

    connection = get_db_connection()

    allocations = connection.execute(
        """
        SELECT *
        FROM allocations
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return render_template(
        "reports.html",
        allocations=allocations
    )


# ============================================================
# DELETE ALLOCATION
# ============================================================

@app.route(
    "/delete/<int:allocation_id>",
    methods=["POST"]
)
def delete_allocation(
    allocation_id
):

    connection = get_db_connection()

    connection.execute(
        """
        DELETE FROM allocations
        WHERE id = ?
        """,
        (allocation_id,)
    )

    connection.commit()

    connection.close()

    return redirect(
        url_for("reports")
    )


# ============================================================
# SETTINGS
# ============================================================

@app.route("/settings")
def settings():

    return render_template(
        "settings.html"
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print(
        "============================================"
    )

    print(
        "      SpectrumSim Application"
    )

    print(
        "============================================"
    )

    print(
        "Server: http://127.0.0.1:5000"
    )

    print(
        "Login : http://127.0.0.1:5000/login"
    )

    print(
        "Settings: http://127.0.0.1:5000/settings"
    )

    print(
        "============================================"
    )


    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )       