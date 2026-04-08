<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%@ page import="java.util.*" %>

<html>
<head>
    <title>Hotel Results</title>
</head>
<body>

<h2>Hotel Results</h2>

<p><b>Location:</b> ${location}</p>
<p><b>Check-in:</b> ${checkin}</p>
<p><b>Check-out:</b> ${checkout}</p>
<p><b>Guests:</b> ${guests}</p>

<hr>

<h3>Available Hotels:</h3>

<%
List<String> list = (List<String>) request.getAttribute("hotelList");

if (list != null && !list.isEmpty()) {
    for (String h : list) {
%>
        <p><%= h %></p>
<%
    }
} else {
%>
    <p>No hotels found</p>
<%
}
%>

</body>
</html>