import java.io.IOException;
import java.sql.*;

import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/CancelBooking")
public class CancelBooking extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String bookingId = request.getParameter("bookingId");
        String busId = request.getParameter("busId");
        String passengers = request.getParameter("passengers");

        try {
         	Class.forName("com.mysql.jdbc.Driver");
			Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/trip","root","abhay@6263");

            
            String cancelQuery = "UPDATE busbookings SET status='CANCELLED' WHERE id=?";
            PreparedStatement ps1 = con.prepareStatement(cancelQuery);
            ps1.setInt(1, Integer.parseInt(bookingId));
            ps1.executeUpdate();

        
            String seatQuery = "UPDATE buses SET seats_available = seats_available + ? WHERE id=?";
            PreparedStatement ps2 = con.prepareStatement(seatQuery);
            ps2.setInt(1, Integer.parseInt(passengers));
            ps2.setInt(2, Integer.parseInt(busId));
            ps2.executeUpdate();

            response.sendRedirect("dashboard.html");

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}