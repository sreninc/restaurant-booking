(function() {
    emailjs.init('user_S6JAlKTkHIee3fsq7Jbum');
})();

// Logic used to load the contact form and emailjs form handling on the about.html page
document.getElementById("contact-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const templateParams = {
        from_name: this.firstName.value,
        email: this.email.value,
        contact_type: this.lastName.value,
        message: this.message.value
    };
    emailjs.send("financial_freedom", "financial_f_contact", templateParams)
        .then(function(response) {
            this.formSubmit.innerHTML = "Form Submitted";
            this.formSubmit.classList.remove("btn-primary");
            this.formSubmit.classList.add("btn-success");
            this.formSubmit.classList.add("disabled");
            this.formSubmit.type = "button";

        }, function(error) {
        });
        this.reset();
});