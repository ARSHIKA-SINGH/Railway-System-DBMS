from dotenv import load_dotenv
load_dotenv()
from decimal import Decimal
from flask import Flask, render_template
import mysql.connector
from config import Config
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)


def get_db_connection():
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DATABASE"],
        port=app.config["MYSQL_PORT"],
    )


def execute_query(query, params=None, fetchone=False):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    data = cursor.fetchone() if fetchone else cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def to_float(value):
    if value is None:
        return 0.0
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


# ---------------- DASHBOARD ----------------
@app.route("/")
@app.route("/dashboard")
def dashboard():
    metrics = execute_query(
        """
        SELECT
            (SELECT COUNT(*) FROM Booking) AS total_bookings,
            (SELECT COUNT(*) FROM Passenger) AS total_passengers,
            (SELECT COALESCE(SUM(fare), 0) FROM Ticket) AS total_revenue,
            (SELECT COALESCE(MAX(fare), 0) FROM Ticket) AS highest_fare
        """,
        fetchone=True,
    )

    metrics["total_revenue"] = to_float(metrics.get("total_revenue"))
    metrics["highest_fare"] = to_float(metrics.get("highest_fare"))

    return render_template("dashboard.html", metrics=metrics)


# ---------------- BOOKINGS ----------------
@app.route("/bookings")
def bookings():
    booking_details = execute_query(
        """
        SELECT name, train_name, booking_date, status
        FROM Booking_Details
        ORDER BY booking_date DESC
        """
    )
    return render_template("bookings.html", booking_details=booking_details)


# ---------------- TICKETS ----------------
@app.route("/tickets")
def tickets():
    ticket_info = execute_query(
        """
        SELECT booking_id, train_name, seat_number, coach_number, fare
        FROM Ticket_Info
        ORDER BY booking_id
        """
    )
    return render_template("tickets.html", ticket_info=ticket_info)


# ---------------- ROUTES ----------------
@app.route("/routes")
def routes():
    route_details = execute_query(
        """
        SELECT train_name, station_name, arrival_time, departure_time
        FROM Route_Details
        ORDER BY train_name, arrival_time
        """
    )
    return render_template("routes.html", route_details=route_details)


# ---------------- ANALYTICS ----------------
@app.route("/analytics")
def analytics():

    # Fare stats
    fare_stats = execute_query(
        """
        SELECT
            COALESCE(AVG(fare), 0) AS avg_fare,
            COALESCE(SUM(fare), 0) AS total_fare
        FROM Ticket
        """,
        fetchone=True,
    )

    # Train-wise bookings
    train_wise_bookings = execute_query(
        """
        SELECT train_id, COUNT(*) AS total_bookings
        FROM Booking
        GROUP BY train_id
        ORDER BY total_bookings DESC
        """
    )

    # Rajdhani passengers (FIXED)
    rajdhani_passengers = execute_query(
        """
        SELECT name, phone
        FROM Passenger
        WHERE passenger_id IN (
            SELECT passenger_id FROM Booking
            WHERE train_id = (
                SELECT train_id FROM Train
                WHERE train_name = 'Rajdhani Express'
            )
        )
        ORDER BY name
        """
    )

    fare_stats["avg_fare"] = to_float(fare_stats.get("avg_fare"))
    fare_stats["total_fare"] = to_float(fare_stats.get("total_fare"))

    return render_template(
        "analytics.html",
        fare_stats=fare_stats,
        train_wise_bookings=train_wise_bookings,
        rajdhani_passengers=rajdhani_passengers,
    )


if __name__ == "__main__":
    app.run(debug=True)