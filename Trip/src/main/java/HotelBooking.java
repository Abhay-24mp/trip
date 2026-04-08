import java.io.IOException;
import java.io.PrintWriter;
import java.sql.*;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/HotelBooking")
public class HotelBooking extends HttpServlet {

    protected void service(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        String fullname  = request.getParameter("fullname");
        String email     = request.getParameter("email");
        String mobile    = request.getParameter("mobile");
        String checkin   = request.getParameter("checkin");
        String checkout  = request.getParameter("checkout");
        String hotelName = request.getParameter("hotelName");

        if (fullname == null || fullname.trim().isEmpty() ||
            email == null || email.trim().isEmpty() ||
            mobile == null || mobile.trim().isEmpty()) {

            RequestDispatcher rd = request.getRequestDispatcher("bookHotel");
            rd.include(request, response);
            out.println("<script>alert('Please fill all required fields!');</script>");
            return;
        }

        Connection con = null;
        PreparedStatement ps = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");
            con = DriverManager.getConnection("jdbc:mysql://localhost:3306/trip","root","abhay@6263");

            //  HOTEL PRICE FETCH
            String priceQuery = "SELECT price_per_night FROM hotels WHERE name = ?";
            PreparedStatement ps1 = con.prepareStatement(priceQuery);
            ps1.setString(1, hotelName);

            ResultSet rs = ps1.executeQuery();

            int pricePerNight = 0;

            if (rs.next()) {
                pricePerNight = rs.getInt("price_per_night");
            }

            // DAYS CALCULATE
            LocalDate d1 = LocalDate.parse(checkin);
            LocalDate d2 = LocalDate.parse(checkout);

            long days = ChronoUnit.DAYS.between(d1, d2);

            if(days <= 0){
                out.println("<script>alert('Invalid Dates!');</script>");
                return;
            }

            //  TOTAL CALCULATE
            long total = days * pricePerNight;

            // INSERT BOOKING (add columns in DB if not exist)
            String query = "INSERT INTO bookings (fullname, email, mobile, hotel_name, checkin, checkout, days, total_amount, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)";

            ps = con.prepareStatement(query);
            ps.setString(1, fullname);
            ps.setString(2, email);
            ps.setString(3, mobile);
            ps.setString(4, hotelName);
            ps.setDate(5, Date.valueOf(checkin));
            ps.setDate(6, Date.valueOf(checkout));
            ps.setLong(7, days);
            ps.setLong(8, total);
            ps.setString(9, "CONFIRMED");

            int rows = ps.executeUpdate();

            if (rows > 0) {
                RequestDispatcher rd = request.getRequestDispatcher("dashboard.html");
                rd.include(request, response);
                out.println("<script>alert('Booking Confirmed! Total: " + total + " ₹');</script>");
            } else {
                RequestDispatcher rd = request.getRequestDispatcher("bookHotel");
                rd.include(request, response);
                out.println("<script>alert('Booking Failed!');</script>");
            }

        } catch (Exception e) {
            out.println("<h3 style='color:red;'>Error: " + e.getMessage() + "</h3>");
            e.printStackTrace();
        } finally {
            try { if (ps != null) ps.close(); } catch (Exception ignored) {}
            try { if (con != null) con.close(); } catch (Exception ignored) {}
        }
    }
}