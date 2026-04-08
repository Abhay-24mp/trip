import java.io.IOException;
import java.io.PrintWriter;
import java.sql.*;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/BusBooking")
public class BusBooking extends HttpServlet {

	protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		
		response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        String fullname = request.getParameter("fullname");
        String mobile   = request.getParameter("mobile");
        String busId    = request.getParameter("busId");
        String passengersStr = request.getParameter("passengers");

       
        if (fullname == null || fullname.trim().isEmpty() ||
            mobile == null || mobile.trim().isEmpty() ||
            busId == null || busId.trim().isEmpty() ||
            passengersStr == null || passengersStr.trim().isEmpty()) {

            RequestDispatcher rd = request.getRequestDispatcher("busForm.jsp");
            rd.include(request, response);
            out.println("<script>alert('Please fill all fields!');</script>");
            return;
        }

        int passengers = Integer.parseInt(passengersStr);

        Connection con = null;
        PreparedStatement ps = null;
        ResultSet rs = null;

        try {
        	Class.forName("com.mysql.jdbc.Driver");
			Connection con1=DriverManager.getConnection("jdbc:mysql://localhost:3306/trip","root","abhay@6263");

            
            String checkQuery = "SELECT seats_available FROM buses WHERE id=?";
            ps = con1.prepareStatement(checkQuery);
            ps.setInt(1, Integer.parseInt(busId));
            rs = ps.executeQuery();

            if (rs.next()) {
                int seats = rs.getInt("seats_available");

                if (seats >= passengers) {  

                    
                    String insertQuery = "INSERT INTO busbookings (name, mobile, bus_id, passengers) VALUES (?, ?, ?, ?)";
                    ps = con1.prepareStatement(insertQuery);
                    ps.setString(1, fullname);
                    ps.setString(2, mobile);
                    ps.setInt(3, Integer.parseInt(busId));
                    ps.setInt(4, passengers);

                    int rows = ps.executeUpdate();

                    if (rows > 0) {

                        
                        String updateQuery = "UPDATE buses SET seats_available = seats_available - ? WHERE id=? AND seats_available >= ?";
                        ps = con1.prepareStatement(updateQuery);
                        ps.setInt(1, passengers);
                        ps.setInt(2, Integer.parseInt(busId));
                        ps.setInt(3, passengers);

                        ps.executeUpdate();

                        RequestDispatcher rd = request.getRequestDispatcher("busindex.html");
                        rd.include(request, response);
                        out.println("<script>alert('Bus Booking Confirmed!');</script>");

                    } else {
                        RequestDispatcher rd = request.getRequestDispatcher("busForm.jsp");
                        rd.include(request, response);
                        out.println("<script>alert('Booking Failed!');</script>");
                    }

                } else {
                    RequestDispatcher rd = request.getRequestDispatcher("busForm.jsp");
                    rd.include(request, response);
                    out.println("<script>alert('Not enough seats available!');</script>");
                }

            } else {
                out.println("<script>alert('Bus Not Found!');</script>");
            }

        } catch (Exception e) {
            out.println("<h3 style='color:red;'>Error: " + e.getMessage() + "</h3>");
        } finally {
            try { if (rs != null) rs.close(); } catch (Exception ignored) {}
            try { if (ps != null) ps.close(); } catch (Exception ignored) {}
            try { if (con != null) con.close(); } catch (Exception ignored) {}
        }
	}
}