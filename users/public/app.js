const registerForm = document.getElementById("registerForm");
const loginForm = document.getElementById("loginForm");

if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const message = document.getElementById("registerMessage");

    try {
      const response = await fetch("/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email, password })
      });

      if (!response.ok) {
        const errorData = await response.json();
        message.textContent = errorData.error || "Napaka pri registraciji.";
        return;
      }

      const user = await response.json();
      message.textContent = `Uporabnik ${user.name} je uspešno ustvarjen.`;
      registerForm.reset();
    } catch (error) {
      message.textContent = "Strežnik ni dosegljiv.";
    }
  });
}

if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    const message = document.getElementById("loginMessage");

    try {
      const response = await fetch("/api/users");
      const users = await response.json();

      const user = users.find(
        (u) => u.email === email && u.password === password
      );

      if (user) {
        message.textContent = `Prijava uspešna. Pozdravljen, ${user.name}!`;
      } else {
        message.textContent = "Napačen email ali geslo.";
      }
    } catch (error) {
      message.textContent = "Strežnik ni dosegljiv.";
    }
  });
}