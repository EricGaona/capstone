document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("sendMoneyForm");
    const messageDiv = document.getElementById("message");
    const validateForm = document.getElementById("validateCodeForm");
    const validateMessageDiv = document.getElementById("validateMessage");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Client-side validation
        if (!data.senderAccountNumber || !data.recipientEmail || !data.amount) {
            messageDiv.innerHTML = "<p style='color: red;'>All fields are required from JS</p>";
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
                messageDiv.innerHTML = `<p style='color: green;'>${result.message}</p>`;
                form.reset(); // Clear the form after successful submission

                setTimeout(() => {
                    messageDiv.innerHTML = "";
                }, 3000); // Clear message after 3 seconds
            } else {
                messageDiv.innerHTML = `<p style='color: red;'>${result.error}</p>`;
            }
        } catch (error) {
            messageDiv.innerHTML = "<p style='color: red;'>An unexpected error occurred.</p>";
        }
    });

    validateForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const formData = new FormData(validateForm);
        const data = Object.fromEntries(formData.entries());

        // Send data to the server using fetch
        try {
            const response = await fetch(validateForm.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                validateMessageDiv.innerHTML = `<p style='color: green;'>Code validated successfully!</p>`;
                validateForm.reset(); // Clear the form after successful validation

                setTimeout(() => {
                    validateMessageDiv.innerHTML = "";
                }, 3000); // Clear message after 3 seconds
            } else {
                validateMessageDiv.innerHTML = `<p style='color: red;'>${result.error}</p>`;
            }
        } catch (error) {
            validateMessageDiv.innerHTML = "<p style='color: red;'>An unexpected error occurred.</p>";
        }
    });
});
