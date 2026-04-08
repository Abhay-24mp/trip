import java.io.IOException;
import java.sql.*;

import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/CarBooking")
public class CarBooking extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String name   = request.getParameter("name");
        String mobile = request.getParameter("mobile");
        String carId  = request.getParameter("carId");
        String daysStr = request.getParameter("days");

        // validation
        if(name == null || name.trim().isEmpty() ||
           mobile == null || mobile.trim().isEmpty() ||
           carId == null || daysStr == null){

            response.getWriter().println("<script>alert('Fill all fields!');history.back();</script>");
            return;
        }

        int days = Integer.parseInt(daysStr);

        if(days <= 0){
            response.getWriter().println("<script>alert('Invalid days!');history.back();</script>");
            return;
        }

        Connection con = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");
            con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/trip", "root", "abhay@6263"
            );

            String priceQuery = "SELECT price FROM cars WHERE id=?";
            PreparedStatement ps1 = con.prepareStatement(priceQuery);
            ps1.setInt(1, Integer.parseInt(carId));

            ResultSet rs = ps1.executeQuery();

            int price = 0;

            if(rs.next()){
                price = rs.getInt("price");
            } else {
                response.getWriter().println("<script>alert('Car not found!');history.back();</script>");
                return;
            }

            
            int total = days * price;

           
            String query = "INSERT INTO carbookings (name, mobile, car_id, days, total_amount, status) VALUES (?, ?, ?, ?, ?, ?)";
            PreparedStatement ps = con.prepareStatement(query);

            ps.setString(1, name);
            ps.setString(2, mobile);
            ps.setInt(3, Integer.parseInt(carId));
            ps.setInt(4, days);
            ps.setInt(5, total);
            ps.setString(6, "CONFIRMED");

            int rows = ps.executeUpdate();

            if(rows > 0){

               
                String update = "UPDATE cars SET available = available - 1 WHERE id=? AND available > 0";
                PreparedStatement ps2 = con.prepareStatement(update);
                ps2.setInt(1, Integer.parseInt(carId));

                int updated = ps2.executeUpdate();

                if(updated > 0){
                	response.getWriter().println("<script>alert('Car Booked! Total: " + total + " '); window.location='dashboard.html';</script>");
                } else {
                    response.getWriter().println("<script>alert('Car not available!');history.back();</script>");
                }
            }

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
            response.getWriter().println("<h3 style='color:red;'>Error: " + e.getMessage() + "</h3>");
        }
    }
}