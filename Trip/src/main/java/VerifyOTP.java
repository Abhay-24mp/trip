import java.io.IOException;
import java.sql.*;

import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;

@WebServlet("/VerifyOTP")
public class VerifyOTP extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String userOtp = request.getParameter("otp");
        String newPass = request.getParameter("newpass");

        HttpSession session = request.getSession();

        int otp = (int) session.getAttribute("otp");
        String email = (String) session.getAttribute("email");

        if (Integer.parseInt(userOtp) == otp) {

            try {
                Class.forName("com.mysql.jdbc.Driver");
                Connection con = DriverManager.getConnection(
                        "jdbc:mysql://localhost:3306/trip", "root", "abhay@6263");

                String query = "UPDATE users SET password=? WHERE email=?";
                PreparedStatement ps = con.prepareStatement(query);

                ps.setString(1, newPass);
                ps.setString(2, email);

                ps.executeUpdate();

                response.getWriter().println("Password Updated Successfully");

                con.close();

            } catch (Exception e) {
                e.printStackTrace();
            }

        } else {
            response.getWriter().println("Invalid OTP");
        }
    }
}