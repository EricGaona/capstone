document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("sendMoneyForm");
    const messageDiv = document.getElementById("message");
    console.log("all good here")

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        console.log("all good here too")
        // Client-side validation
        if (!data.senderAccountNumber || !data.recipientEmail || !data.amount) {
            messageDiv.innerHTML = "<p style='color: red;'>All fields are required from JS</p>";

            return;
        }
        console.log(typeof (data.amount));

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
                    messageDiv.innerHTML = " ";

                }, 3000); // Redirect after 2 seconds
                // Optionally redirect or perform other actions here if needed
            } else {
                messageDiv.innerHTML = `<p style='color: red;'>${result.error}</p>`;
                //    messageDiv.innerHTML = `<p style='color: red;'>The email <b>${data.recipientEmail}</b> does not exist or it is your own email.</p>`;
            }
        } catch (error) {
            console.log("entro aqui");

            messageDiv.innerHTML = "<p style='color: red;'>An unexpected error occurred.</p>";
        }
    });
});
