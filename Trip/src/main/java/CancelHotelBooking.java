import java.io.IOException;
import java.sql.*;

import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/CancelHotelBooking")
public class CancelHotelBooking extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String bookingId = request.getParameter("bookingId");

        try {
            Class.forName("com.mysql.jdbc.Driver");

            Connection con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/trip", "root", "abhay@6263"
            );

            String query = "UPDATE bookings SET status='CANCELLED' WHERE id=?";
            PreparedStatement ps = con.prepareStatement(query);
            ps.setInt(1, Integer.parseInt(bookingId));

            ps.executeUpdate();

            response.sendRedirect("dashboard.html");

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}