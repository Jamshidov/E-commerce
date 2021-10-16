'use strict';

let rlink = document.getElementById("register_link");
let llink = document.getElementById("login_link");

let regblock = document.getElementById("register");
let logblock = document.getElementById("login");

regblock.style.display = "block";
logblock.style.display = "none";

rlink.addEventListener('click', () => {
    regblock.style.display = "block";
    logblock.style.display = "none";
})

llink.addEventListener('click', () => {
    logblock.style.display = "block";
    regblock.style.display = "none";
})

