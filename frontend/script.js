let user = null;

/* =========================
   TOGGLE AUTH SCREENS
========================= */
function showLogin() {
  document.getElementById("loginBox").classList.remove("hidden");
  document.getElementById("signupBox").classList.add("hidden");
}

function showSignup() {
  document.getElementById("signupBox").classList.remove("hidden");
  document.getElementById("loginBox").classList.add("hidden");
}

/* =========================
   SIGNUP (SAVE USER)
========================= */
function signup() {
  let u = document.getElementById("signupUser").value.trim();
  let p = document.getElementById("signupPass").value.trim();

  if (!u || !p) {
    alert("Please fill all fields");
    return;
  }

  if (localStorage.getItem(u)) {
    alert("User already exists");
    return;
  }

  localStorage.setItem(u, p);

  alert("Account created successfully");

  showLogin();
}

/* =========================
   LOGIN
========================= */
function login() {
  let u = document.getElementById("loginUser").value.trim();
  let p = document.getElementById("loginPass").value.trim();

  if (!u || !p) {
    alert("Please fill all fields");
    return;
  }

  let stored = localStorage.getItem(u);

  if (stored && stored === p) {
    user = u;

    document.getElementById("auth").classList.add("hidden");
    document.getElementById("dashboard").classList.remove("hidden");
    document.getElementById("navbar").classList.remove("hidden");

    document.getElementById("user").innerText = u;

    // clear inputs
    document.getElementById("loginUser").value = "";
    document.getElementById("loginPass").value = "";

  } else {
    alert("Invalid username or password");
  }
}

/* =========================
   UPLOAD (DUMMY FOR NOW)
========================= */
function upload() {
  let file = document.getElementById("file").files[0];

  if (!file) {
    alert("Please select a file");
    return;
  }

  document.getElementById("result").innerText =
    "Processing " + file.name + "...\n\nAI: Analyzing report...";

  // simulate AI delay
  setTimeout(() => {
    document.getElementById("result").innerText =
      "✔ Report Processed\n\nAI Summary:\n- Patient condition stable\n- No major abnormalities detected";
  }, 1500);
}

/* =========================
   PROFILE MENU
========================= */
function toggleMenu() {
  document.getElementById("menu").classList.toggle("hidden");
}

/* =========================
   LOGOUT
========================= */
function logout() {
  user = null;

  document.getElementById("auth").classList.remove("hidden");
  document.getElementById("dashboard").classList.add("hidden");
  document.getElementById("navbar").classList.add("hidden");

  document.getElementById("menu").classList.add("hidden");
}