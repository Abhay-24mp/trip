// ---------- INITIAL DATA ----------

if(!localStorage.getItem("hotels")){

localStorage.setItem("hotels", JSON.stringify([

{
name:"Sea View Resort",
location:"Goa",
price:4500,
rating:"⭐⭐⭐⭐",
image:"https://images.unsplash.com/photo-1566073771259-6a8506099945"
},

{
name:"Mountain Paradise",
location:"Manali",
price:3800,
rating:"⭐⭐⭐⭐⭐",
image:"https://images.unsplash.com/photo-1582719478250-c89cae4dc85b"
},

{
name:"Royal Palace Hotel",
location:"Jaipur",
price:4200,
rating:"⭐⭐⭐⭐",
image:"https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-4.0.3&w=1080&fit=crop&q=80&fm=jpg"
}

]))

}


if(!localStorage.getItem("cars")){

localStorage.setItem("cars", JSON.stringify([

{
name:"Toyota Innova",
price:3200,
seats:7,
fuel:"Diesel",
image:"https://images.unsplash.com/photo-1503376780353-7e6692767b70"
},

{
name:"Swift Dzire",
price:1800,
seats:5,
fuel:"Petrol",
image:"https://images.unsplash.com/photo-1549921296-3a6b9a4f3b0a"
}

]))

}


if(!localStorage.getItem("buses")){

localStorage.setItem("buses", JSON.stringify([

{
name:"Luxury Volvo Bus",
route:"Delhi → Jaipur",
price:15000,
capacity:40
},

{
name:"Tourist Coach",
route:"Delhi → Manali",
price:18000,
capacity:35
}

]))

}



// ---------- REGISTER ----------

function registerUser(){

let name=document.getElementById("name").value
let email=document.getElementById("email").value
let password=document.getElementById("password").value

let users=JSON.parse(localStorage.getItem("users"))||[]

users.push({name,email,password})

localStorage.setItem("users",JSON.stringify(users))

alert("Account created!")

location="login.html"

}


// ---------- LOGIN ----------

function loginUser(){

let email=document.getElementById("email").value
let password=document.getElementById("password").value

let users=JSON.parse(localStorage.getItem("users"))||[]

let user=users.find(u=>u.email===email && u.password===password)

if(user){

localStorage.setItem("activeUser",email)

location="dashboard.html"

}else{

alert("Invalid Login")

}

}


// ---------- LOGOUT ----------

function logout(){

localStorage.removeItem("activeUser")

location="index.html"

}



// ---------- BOOKING ----------

function bookService(name,type){

let bookings=JSON.parse(localStorage.getItem("bookings"))||[]

bookings.push({

name:name,
type:type,
date:new Date().toLocaleDateString()

})

localStorage.setItem("bookings",JSON.stringify(bookings))

showToast()

}



// ---------- TOAST ----------

function showToast(){

let toast=document.getElementById("toast")

if(toast){

toast.style.display="block"

setTimeout(()=>{

toast.style.display="none"

},2000)

}

}

function filterHotels(){

let input=document.getElementById("filterInput").value.toLowerCase()

let cards=document.querySelectorAll(".card")

cards.forEach(card=>{

let text=card.innerText.toLowerCase()

card.style.display=text.includes(input)?"block":"none"

})

}

/* --- MOBILE MENU TOGGLE --- */
document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('mobile-menu');
    const navLinks = document.getElementById('nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = menuToggle.querySelector('i');
            if (icon.classList.contains('bi-list')) {
                icon.classList.remove('bi-list');
                icon.classList.add('bi-x-lg');
            } else {
                icon.classList.remove('bi-x-lg');
                icon.classList.add('bi-list');
            }
        });
    }
});