console.log("Hello, World 6!!!");

// document.addEventListener("DOMContentLoaded", () => {
//     const form = document.getElementById("registerForm");
//     const messageDiv = document.getElementById("message");

//     form.addEventListener("submit", async (event) => {
//       event.preventDefault(); // Prevent the default form submission

//       // Get form data
//       const formData = new FormData(form);
//       const data = Object.fromEntries(formData.entries());

//       // Client-side validation
//       if (!data.userName || !data.firstName || !data.lastName || !data.email || !data.phoneNumber || !data.address || !data.password || !data.confirmPassword) {
//         messageDiv.innerHTML = "<p style='color: red;'>All fields are required.</p>";
//         return;
//       }

//       if (data.password !== data.confirmPassword) {
//         messageDiv.innerHTML = "<p style='color: red;'>Passwords do not match.</p>";
//         return;
//       }

//       // Send data to the server using fetch
//       try {
//         const response = await fetch(form.action, {
//           method: "POST",
//           headers: {
//             "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
//             "Content-Type": "application/json",
//           },
//           body: JSON.stringify(data),
//         });

//         const result = await response.json();

//         if (response.ok) {
//           messageDiv.innerHTML = `<p style='color: green;'>${result.message} Your account number is: ${result.accountNumber}</p>`;
//           form.reset(); // Clear the form after successful submission
//         } else {
//           messageDiv.innerHTML = `<p style='color: red;'>${result.error}</p>`;
//         }
//       } catch (error) {
//         console.error("Error:", error);
//         messageDiv.innerHTML = "<p style='color: red;'>An unexpected error occurred.</p>";
//       }
//     });
//   });


document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");
    const messageDiv = document.getElementById("message");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Client-side validation
        if (!data.firstName || !data.lastName || !data.email || !data.phoneNumber || !data.address || !data.password || !data.confirmPassword) {
            messageDiv.innerHTML = "<p style='color: red;'>All fields are required.</p>";
            return;
        }

        if (data.password !== data.confirmPassword) {
            messageDiv.innerHTML = "<p style='color: red;'>Passwords do not match.</p>";
            return;
        }

        // Send data to the server using fetch
        try {
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                // messageDiv.innerHTML = `<p style='color: green;'>${result.message} Your account number is: ${result.accountNumber}</p>`;

                // Redirect to index.html after successful registration
                // setTimeout(() => {
                    window.location.href = "http://127.0.0.1:8000";
                    await new Promise(r => setTimeout(r, 1000));
                    form.reset(); // Clear the form after successful submission

                // }, 1); // Redirect after 2 seconds
            } else {
                messageDiv.innerHTML = `<p style='color: red;'>${result.error}</p>`;
            }
        } catch (error) {
            console.error("Error:", error);
            messageDiv.innerHTML = "<p style='color: red;'>An unexpected error occurred.</p>";
        }
    });
});
