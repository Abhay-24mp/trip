import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;

import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/ViewBookings")
public class ViewBookings extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String mobile = request.getParameter("mobile");

        ArrayList<String[]> list = new ArrayList<>();
        ArrayList<String[]> history = new ArrayList<>();

        try {
        	Class.forName("com.mysql.jdbc.Driver");
			Connection con=DriverManager.getConnection("jdbc:mysql://localhost:3306/trip","root","abhay@6263");


           
			String busQuery = "SELECT b.id, b.bus_id, bs.bus_name, bs.from_city, bs.to_city, bs.travel_date, b.passengers, b.status " +
	                  "FROM busbookings b JOIN buses bs ON b.bus_id = bs.id " +
	                  "WHERE b.mobile=? AND b.status!='CANCELLED'";

            PreparedStatement ps1 = con.prepareStatement(busQuery);
            ps1.setString(1, mobile);
            ResultSet rs1 = ps1.executeQuery();

            while (rs1.next()) {
                String data[] = new String[9];

                data[0] = "BUS";
                data[1] = rs1.getString("bus_name");
                data[2] = rs1.getString("from_city");
                data[3] = rs1.getString("to_city");
                data[4] = rs1.getString("travel_date");
                data[5] = rs1.getString("passengers");
                data[6] = rs1.getString("status");
                data[7] = rs1.getString("id");      
                data[8] = rs1.getString("bus_id");  

                list.add(data);
            }

            
            String hotelQuery = "SELECT id, hotel_name, checkin, checkout, status FROM bookings WHERE mobile=? AND status!='CANCELLED'";
            
            PreparedStatement ps2 = con.prepareStatement(hotelQuery);
            ps2.setString(1, mobile);
            ResultSet rs2 = ps2.executeQuery();

            while (rs2.next()) {
                String data[] = new String[9];

                data[0] = "HOTEL";
                data[1] = rs2.getString("hotel_name");
                data[2] = rs2.getString("checkin");
                data[3] = rs2.getString("checkout");
                data[4] = "-";
                data[5] = "-";
                data[6] = rs2.getString("status");
                data[7] = rs2.getString("id");   
                data[8] = "0";

                list.add(data);
            }
            
            
        
            String carQuery = "SELECT cb.id, c.car_name, c.city, cb.days, cb.status, cb.car_id " +
                              "FROM carbookings cb JOIN cars c ON cb.car_id = c.id " +
                              "WHERE cb.mobile=? AND cb.status!='CANCELLED'";

            PreparedStatement ps3 = con.prepareStatement(carQuery);
            ps3.setString(1, mobile);

            ResultSet rs3 = ps3.executeQuery();

            while(rs3.next()){
                String[] c = new String[9];

                c[0] = "CAR";
                c[1] = rs3.getString("car_name");
                c[2] = rs3.getString("city");
                c[3] = rs3.getString("days");
                c[4] = rs3.getString("status");
                c[5] = rs3.getString("id");      
                c[6] = rs3.getString("car_id");  
                c[7] = "-";
                c[8] = "-";

                list.add(c); 
            }

            request.setAttribute("history", list);
            RequestDispatcher rd = request.getRequestDispatcher("bookingHistory.jsp");
            rd.forward(request, response);

            con.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}