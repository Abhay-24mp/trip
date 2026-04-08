import java.io.IOException;
import java.util.ArrayList;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.sql.*;

@WebServlet("/SearchCar")
public class SearchCar extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String city = request.getParameter("city");

        ArrayList<String[]> cars = new ArrayList<>();

        try {
            Class.forName("com.mysql.jdbc.Driver");
            Connection con = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/trip", "root", "abhay@6263");

            String query = "SELECT * FROM cars WHERE city=?";
            PreparedStatement ps = con.prepareStatement(query);
            ps.setString(1, city);

            ResultSet rs = ps.executeQuery();

            while (rs.next()) {
            	String[] c = new String[8];

            	c[0] = rs.getString("id");
            	c[1] = rs.getString("car_name");
            	c[2] = rs.getString("city");
            	c[3] = rs.getString("price_per_day");
            	c[4] = rs.getString("seats");
            	c[5] = rs.getString("fuel_type");
            	c[6] = rs.getString("transmission");
            	c[7] = rs.getString("available");

            	cars.add(c);
            }

            request.setAttribute("cars", cars);
            RequestDispatcher rd = request.getRequestDispatcher("carList.jsp");
            rd.forward(request, response);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}