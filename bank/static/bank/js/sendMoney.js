document.addEventListener("DOMContentLoaded", () => {
    const sendMoneyForm = document.getElementById("sendMoneyForm");
    const messageDiv = document.getElementById("message");

    const validateCodeForm = document.getElementById("validateCodeForm");
    const validateMessageDiv = document.getElementById("validateMessage");

    validateCodeForm.style.display = "none";

    sendMoneyForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const formData = new FormData(sendMoneyForm);
        const data = Object.fromEntries(formData.entries());

        // Client-side validation
        if (!data.senderAccountNumber || !data.recipientEmail || !data.amount) {
            messageDiv.innerHTML = "<p style='color: red;'>All fields are required from JS</p>";
            return;
        }

        // Send data to the server using fetch
        try {
            const response = await fetch(sendMoneyForm.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                // messageDiv.innerHTML = `<p style='color: green;'>${result.message}</p>`;
                validateCodeForm.style.display = "block"; // Show the validation form
                sendMoneyForm.style.display = "none";
                messageDiv.innerHTML = "";

            } else {
                messageDiv.innerHTML = `<p style='color: red;'>${result.error}</p>`;
            }
        } catch (error) {
            messageDiv.innerHTML = "<p style='color: red;'>An unexpected error occurred.</p>";
        }
    });

    // --------------------------------------------------------------------------------------------------------------------
    validateCodeForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const formData = new FormData(validateCodeForm);
        const data = Object.fromEntries(formData.entries());

        // Send data to the server using fetch
        try {
            const response = await fetch(validateCodeForm.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                validateMessageDiv.innerHTML = `<p style='color: green;'>Money sent successfully!</p>`;

                setTimeout(() => {
                    validateCodeForm.reset();
                    validateCodeForm.style.display = "none";

                    sendMoneyForm.reset(); // Clear the send money form after successful transfer

                    sendMoneyForm.style.display = "block";

                    validateMessageDiv.innerHTML = "";

                }, 6000); // Clear message after 3 seconds
 
            } else {

                validateMessageDiv.innerHTML = `<p style='color: red;'>${result.error}</p>`;

                setTimeout(() => {
                    validateCodeForm.reset();
                    validateCodeForm.style.display = "none";

                    sendMoneyForm.reset(); // Clear the send money form after successful transfer

                    sendMoneyForm.style.display = "block";

                    validateMessageDiv.innerHTML = ""; 

                }, 6000); // Clear message after 3 seconds

            }

        } catch (error) {
            validateMessageDiv.innerHTML = "<p style='color: red;'>An unexpected error occurred.</p>";
        }
    });
});