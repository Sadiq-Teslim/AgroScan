const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const mainRoutes = document.getElementById("main-routes");
const loginUrl = authRoutes.dataset.loginUrl;
const signupUrl = authRoutes.dataset.signupUrl;
const diagnosisUrl = authRoutes.dataset.diagnosisUrl;
    
function isPasswordStrong(password) {
return password.length >= 8 &&
        /[A-Z]/.test(password) &&
        /[a-z]/.test(password) &&
        /[0-9]/.test(password);
}