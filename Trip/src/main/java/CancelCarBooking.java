

import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.sql.*;

@WebServlet("/CancelCarBooking")
public class CancelCarBooking extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String bookingId = request.getParameter("bookingId");
        String carId = request.getParameter("carId");

        try {
            Class.forName("com.mysql.jdbc.Driver");
            Connection con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/trip", "root", "abhay@6263"
            );

            // cancel booking
            String q1 = "UPDATE carbookings SET status='CANCELLED' WHERE id=?";
            PreparedStatement ps1 = con.prepareStatement(q1);
            ps1.setInt(1, Integer.parseInt(bookingId));
            ps1.executeUpdate();

            // restore availability
            String q2 = "UPDATE cars SET available = available + 1 WHERE id=?";
            PreparedStatement ps2 = con.prepareStatement(q2);
            ps2.setInt(1, Integer.parseInt(carId));
            ps2.executeUpdate();

            response.sendRedirect("ViewBookings?mobile=" + request.getParameter("mobile"));

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}