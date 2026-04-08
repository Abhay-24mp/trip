import java.io.IOException;
import java.io.PrintWriter;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import jakarta.servlet.RequestDispatcher;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

@WebServlet("/Ulog")
public class Ulog extends HttpServlet {
    protected void service(HttpServletRequest request, HttpServletResponse response) 
            throws ServletException, IOException {
        
        response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        
        String email = request.getParameter("email");
        String password = request.getParameter("password");
        
        Connection con = null;
        PreparedStatement ps = null;
        ResultSet rs = null;
        
        try {
            Class.forName("com.mysql.jdbc.Driver");
            con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/trip", "root", "abhay@6263"
            );
            
            String q = "SELECT * FROM users WHERE email = ? AND password = ?";
            ps = con.prepareStatement(q);
            ps.setString(1, email);
            ps.setString(2, password);
            
            rs = ps.executeQuery();
            
            if (rs.next()) {
                RequestDispatcher rd = request.getRequestDispatcher("dashboard.html");
                rd.include(request, response);
                out.println("<script>alert('Successfully Logged In!');</script>");
            } else {
                RequestDispatcher rd = request.getRequestDispatcher("login.html");
                rd.include(request, response);
                out.println("<script>alert('Invalid Email or Password');</script>");
            }
            
        } catch (ClassNotFoundException e) {
            out.println("<h3>Driver Not Found: " + e.getMessage() + "</h3>");
            e.printStackTrace();
        } catch (SQLException e) {
            out.println("<h3>Database Error: " + e.getMessage() + "</h3>");
            e.printStackTrace();
        } finally {
            // Close resources
            try { if (rs != null) rs.close(); } catch (Exception e) {}
            try { if (ps != null) ps.close(); } catch (Exception e) {}
            try { if (con != null) con.close(); } catch (Exception e) {}
        }
    }
}