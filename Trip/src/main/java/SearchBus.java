import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;

import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/SearchBus")
public class SearchBus extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String from = request.getParameter("from");
        String to   = request.getParameter("to");
        String date = request.getParameter("date");

        if(from != null) from = from.trim();
        if(to != null) to = to.trim();

        ArrayList<String[]> busList = new ArrayList<>();

        try {
            Class.forName("com.mysql.jdbc.Driver");
            Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/trip","root","abhay@6263");

            
            String query = "SELECT * FROM buses WHERE LOWER(from_city)=LOWER(?) AND LOWER(to_city)=LOWER(?) AND seats_available > 0";

            PreparedStatement ps = con.prepareStatement(query);
            ps.setString(1, from);
            ps.setString(2, to);

            ResultSet rs = ps.executeQuery();

            while (rs.next()) {

                String data[] = new String[10];

                data[0] = rs.getString("id");
                data[1] = rs.getString("bus_name");
                data[2] = rs.getString("bus_type");
                data[3] = rs.getString("seats_available");

                
                data[4] = date;

                data[5] = rs.getString("from_city");
                data[6] = rs.getString("to_city");
                data[7] = rs.getString("departure_time");
                data[8] = rs.getString("arrival_time");

                
                data[9] = rs.getString("price");

                busList.add(data);
            }

            request.setAttribute("buses", busList);
            RequestDispatcher rd = request.getRequestDispatcher("/busList.jsp");
            rd.forward(request, response);

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
            response.getWriter().println("<h2>Error: " + e.getMessage() + "</h2>");
        }
    }
}