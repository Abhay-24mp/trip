import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/HotelSearch")
public class HotelSearch extends HttpServlet {

    protected void service(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        String location = request.getParameter("location");
        String checkin  = request.getParameter("checkin");
        String checkout = request.getParameter("checkout");
        String guests   = request.getParameter("guests");

        
        if (location == null || location.trim().isEmpty() ||
            checkin == null  || checkin.trim().isEmpty()  ||
            checkout == null || checkout.trim().isEmpty()) {

            RequestDispatcher rd = request.getRequestDispatcher("hotels.jsp");
            rd.include(request, response);
            out.println("<script>alert('Please fill Location, Check-in and Check-out dates!');</script>");
            return;
        }

        int guestCount = 1;
        if (guests != null && !guests.isEmpty()) {
            guestCount = Integer.parseInt(guests);
        }

        Connection con = null;
        PreparedStatement ps = null;
        ResultSet rs = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");

            con = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/trip",
                    "root",
                    "abhay@6263"
            );

            
            String q = "SELECT * FROM hotels WHERE LOWER(location) LIKE LOWER(?) AND max_guests >= ?";

            ps = con.prepareStatement(q);
            ps.setString(1, "%" + location.trim() + "%");
            ps.setInt(2, guestCount);

            rs = ps.executeQuery();

            //  List create
            List<String> hotelList = new ArrayList<>();

            while (rs.next()) {
                String name = rs.getString("name");
                double price = rs.getDouble("price_per_night");

                hotelList.add(name + " - ₹" + price);
            }

            if (!hotelList.isEmpty()) {

                request.setAttribute("hotelList", hotelList);
                request.setAttribute("location", location);
                request.setAttribute("checkin", checkin);
                request.setAttribute("checkout", checkout);
                request.setAttribute("guests", guests);

                RequestDispatcher rd = request.getRequestDispatcher("results.jsp");
                rd.forward(request, response);

            } else {
                RequestDispatcher rd = request.getRequestDispatcher("hotels.jsp");
                rd.include(request, response);
                out.println("<script>alert('No hotels found!');</script>");
            }

        } catch (Exception e) {
            e.printStackTrace();
            out.println("<h3>Error: " + e.getMessage() + "</h3>");
        } finally {
            try { if (rs != null) rs.close(); } catch (Exception ignored) {}
            try { if (ps != null) ps.close(); } catch (Exception ignored) {}
            try { if (con != null) con.close(); } catch (Exception ignored) {}
        }
    }
}