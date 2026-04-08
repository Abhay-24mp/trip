<%@ page language="java" contentType="text/html; charset=UTF-8" %>
<%@ page import="java.util.*" %>

<!DOCTYPE html>
<html>
<head>
    <title>Available Buses - Trip Connect</title>

    <style>
        body {
            font-family: Arial;
            background: #f4f6f9;
        }
        .bus-card {
            width: 600px;
            margin: 20px auto;
            background: white;
            padding: 15px;
            border-radius: 10px;
        }
        button {
            padding: 8px 15px;
            background: green;
            color: white;
            border: none;
        }
        input {
            margin: 5px 0;
        }
    </style>

    <!-- 🔥 JS -->
    <script>
    function updateTotal(busId, price) {

        let passengers = document.getElementById("passengers_" + busId).value;

        let total = passengers * price;

        document.getElementById("total_" + busId).value = total + " ₹";
    }
    </script>

</head>

<body>

<h2 style="text-align:center;">Available Buses</h2>

<%
    ArrayList<String[]> buses = (ArrayList<String[]>) request.getAttribute("buses");

    if (buses != null && !buses.isEmpty()) {
        for (String[] b : buses) {

            int price = Integer.parseInt(b[9]); // ⚠️ price index (ensure backend me bhej raha hai)
%>

<div class="bus-card">
    <h3><%= b[1] %> (<%= b[6] %>)</h3>
    <p><b>Route:</b> <%= b[2] %> → <%= b[3] %></p>
    <p><b>Time:</b> 🕒 <%= b[7] %> → <%= b[8] %></p>
    <p>Date: <%= b[4] %></p>
    <p>Seats Available: <%= b[5] %></p>

    <!-- 💰 PRICE -->
    <p><b>Price per person:</b> ₹ <%= price %></p>

    <!-- 🔥 Book Form -->
    <form action="BusBooking" method="post">

        <input type="hidden" name="busId" value="<%= b[0] %>">
        <input type="hidden" name="price" value="<%= price %>">

        Name: <input type="text" name="fullname" required><br>
        Mobile: <input type="text" name="mobile" required><br>

        <!-- 👇 Passenger -->
        Passengers: 
        <input type="number" 
               id="passengers_<%= b[0] %>" 
               name="passengers" 
               min="1" 
               value="1"
               onchange="updateTotal('<%= b[0] %>', <%= price %>)" required><br>

        <!-- 💸 TOTAL -->
        Total:
        <input type="text" 
               id="total_<%= b[0] %>" 
               readonly 
               value="<%= price %> ₹"><br><br>

        <button type="submit">Book Now</button>
    </form>
</div>

<%
        }
    } else {
%>

<h3 style="text-align:center; color:red;">No Buses Available ❌</h3>

<%
    }
%>

</body>
</html>