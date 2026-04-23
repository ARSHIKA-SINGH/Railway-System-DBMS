from decimal import Decimal

from flask import Flask, render_template
import mysql.connector

from config import Config

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


@app.route("/")
@app.route("/dashboard")
def dashboard():
    metrics = execute_query(
        """
        SELECT
            (SELECT COUNT(*) FROM Booking) AS total_bookings,
            (SELECT COUNT(*) FROM Passenger) AS total_passengers,
            (SELECT COALESCE(SUM(Fare), 0) FROM Ticket) AS total_revenue,
            (SELECT COALESCE(MAX(Fare), 0) FROM Ticket) AS highest_fare
        """,
        fetchone=True,
    )

    metrics["total_revenue"] = to_float(metrics.get("total_revenue"))
    metrics["highest_fare"] = to_float(metrics.get("highest_fare"))

    return render_template("dashboard.html", metrics=metrics)


@app.route("/bookings")
def bookings():
    booking_details = execute_query(
        """
        SELECT Passenger_Name, Train_Name, Booking_Date, Booking_Status
        FROM Booking_Details
        ORDER BY Booking_Date DESC
        """
    )
    return render_template("bookings.html", booking_details=booking_details)


@app.route("/tickets")
def tickets():
    ticket_info = execute_query(
        """
        SELECT Booking_ID, Train_Name, Seat_Number, Coach_Number, Fare
        FROM Ticket_Info
        ORDER BY Booking_ID
        """
    )
    return render_template("tickets.html", ticket_info=ticket_info)


@app.route("/routes")
def routes():
    route_details = execute_query(
        """
        SELECT Train_Name, Station_Name, Arrival_Time, Departure_Time
        FROM Route_Details
        ORDER BY Train_Name, Arrival_Time
        """
    )
    return render_template("routes.html", route_details=route_details)


@app.route("/analytics")
def analytics():
    fare_stats = execute_query(
        """
        SELECT
            COALESCE(AVG(Fare), 0) AS avg_fare,
            COALESCE(SUM(Fare), 0) AS total_fare
        FROM Ticket
        """,
        fetchone=True,
    )

    train_wise_bookings = execute_query(
        """
        SELECT tr.Train_Name, COUNT(*) AS booking_count
        FROM Booking b
        JOIN Train tr ON b.Train_ID = tr.Train_ID
        GROUP BY tr.Train_ID, tr.Train_Name
        ORDER BY booking_count DESC, tr.Train_Name ASC
        """
    )

    rajdhani_passengers = execute_query(
        """
        SELECT p.Passenger_Name, p.Contact_Number, p.Email
        FROM Passenger p
        WHERE p.Passenger_ID IN (
            SELECT b.Passenger_ID
            FROM Booking b
            WHERE b.Train_ID = (
                SELECT Train_ID
                FROM Train
                WHERE Train_Name = 'Rajdhani Express'
                LIMIT 1
            )
        )
        ORDER BY p.Passenger_Name
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
