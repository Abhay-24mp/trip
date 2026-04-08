import os

css = """

/* --- TRIPCONNECT CUSTOM RESPONSIVE CSS --- */
body {
    margin: 0;
    padding: 0;
    font-family: 'Poppins', sans-serif;
    background-color: #f8f9fa;
    color: #333;
}

/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 5%;
    background: rgba(255, 255, 255, 0.9);
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    backdrop-filter: blur(10px);
}
.navbar .logo {
    font-size: 1.8rem;
    font-weight: 600;
    color: #ff7a18;
}
.nav-links {
    list-style: none;
    display: flex;
    gap: 20px;
    margin: 0;
    padding: 0;
}
.nav-links li a {
    text-decoration: none;
    font-weight: 500;
    color: #333;
    transition: 0.3s;
}
.nav-links li a:hover {
    color: #ff7a18;
}

/* Hero Section */
.hero {
    height: 80vh;
    background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1506012787146-f92b2d7d6d96?auto=format&fit=crop&w=1920&q=80') center/cover;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    color: white;
    padding: 0 20px;
}
.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 15px;
    font-weight: 600;
}
.hero p {
    font-size: 1.2rem;
    margin-bottom: 30px;
}

/* Search Box */
.search-box {
    display: flex;
    gap: 10px;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(15px);
    padding: 20px;
    border-radius: 15px;
    width: 100%;
    max-width: 600px;
    flex-wrap: wrap;
}
.search-box input {
    flex: 1;
    min-width: 200px;
    padding: 15px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    outline: none;
}
.search-box button {
    padding: 15px 30px;
    background: #ff7a18;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    cursor: pointer;
    font-weight: 500;
    transition: 0.3s;
}
.search-box button:hover {
    background: #e06912;
}

/* Sections */
section:not(.hero) {
    padding: 60px 5%;
    text-align: center;
}
section h2 {
    font-size: 2.2rem;
    margin-bottom: 40px;
    color: #222;
}

/* Grid Layout (Naturally Responsive) */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
}

/* Cards */
.card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    transition: transform 0.3s;
}
.card:hover {
    transform: translateY(-5px);
}
.card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}
.card h3 {
    margin: 20px 0 5px;
}
.card p {
    color: #666;
    margin-bottom: 20px;
}
.card .btn {
    display: inline-block;
    padding: 10px 20px;
    background: #ff7a18;
    color: white;
    text-decoration: none;
    border-radius: 6px;
    margin-bottom: 20px;
    transition: 0.3s;
}
.card .btn:hover {
    background: #e06912;
}
.service-card {
    padding-top: 20px;
}
.service-card h3 {
    font-size: 1.5rem;
}

/* Stats */
.stats .card {
    padding: 30px 20px;
    background: #fff;
}
.stats .card h2 {
    font-size: 2.5rem;
    color: #ff7a18;
    margin-bottom: 10px;
}
.stats .card p {
    font-size: 1.1rem;
    margin: 0;
}

/* Footer */
footer {
    background: #222;
    color: white;
    text-align: center;
    padding: 20px;
    margin-top: 40px;
}

/* Toast */
.toast {
    position: fixed;
    bottom: -100px;
    left: 50%;
    transform: translateX(-50%);
    background: #28a745;
    color: white;
    padding: 15px 30px;
    border-radius: 50px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    transition: 0.5s;
    opacity: 0;
    z-index: 2000;
}
.toast.show {
    bottom: 30px;
    opacity: 1;
}

/* Responsive Overrides */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 15px;
    }
    .hero h1 {
        font-size: 2.5rem;
    }
    .search-box {
        flex-direction: column;
    }
    .search-box input, .search-box button {
        width: 100%;
    }
}
"""

filepath = "Trip_Flask/static/css/style.css"
with open(filepath, "a") as f:
    f.write(css)

