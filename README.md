<h1 align="center">
   🚆 Railway System Database Management System
</h1>

<p align="center">
  <b>A complete DBMS project implementing real-world railway operations using SQL</b>
</p>

<p align="center">
  💾 MySQL • 🧠 DBMS Concepts • 📊 SQL Queries • ⚙️ Views • 🔗 Relationships
</p>

---

## 📌 Overview

The **Railway System Database** is a structured DBMS project designed to manage railway operations such as passengers, bookings, tickets, trains, routes, and stations efficiently.

It demonstrates how real-world systems use relational databases to maintain **data consistency, integrity, and scalability**.

---
## 🚀 Key Features

* ✔️ Structured relational database design
* ✔️ Implementation of Primary & Foreign Keys
* ✔️ Normalization up to **3NF**
* ✔️ Real-world data simulation
* ✔️ SQL Queries:

  * Joins
  * Subqueries
  * Aggregate Functions
  * Group By
* ✔️ Creation of Views

---

## 🧠 Database Schema

### 📂 Tables Included

| Table Name | Description                |
| ---------- | -------------------------- |
| Passenger  | Stores passenger details   |
| Booking    | Stores reservation details |
| Ticket     | Stores ticket & fare info  |
| Train      | Stores train information   |
| Route      | Stores route & stops       |
| Station    | Stores station details     |

---

## 🔗 Relationships

* One Passenger → Multiple Bookings
* One Booking → One Ticket
* Many Bookings → One Train
* One Train → Multiple Routes
* Each Route → One Station

---

## ⚙️ Technologies Used

* 💾 MySQL Workbench
* 🧾 SQL

---

## 📊 SQL Implementation

```sql
SELECT p.name, t.train_name
FROM Passenger p
JOIN Booking b ON p.passenger_id = b.passenger_id
JOIN Train t ON b.train_id = t.train_id;
```

---

## 👁️ Views Created

* Booking_Details
* Ticket_Info
* Route_Details

---

## 🏆 Highlights

* ✨ Clean schema design
* ✨ Practical implementation
* ✨ Industry-relevant concepts
* ✨ Easy to understand and extend

---

## 🚀 How to Run

1️⃣ Open MySQL Workbench

2️⃣ Create database:

```sql
CREATE DATABASE railwaydb;
USE railwaydb;
```

3️⃣ Run SQL script

4️⃣ Execute queries

5️⃣ View results

---
---

## 💡 Learning Outcomes

* ✔️ Database design using ER concepts
* ✔️ SQL query writing
* ✔️ Normalization (3NF)
* ✔️ Real-world DBMS implementation

---

## 👤 Author

**Arshika Singh**

---

<p align="center">
⭐ Star this repository if you found it useful!
</p>
