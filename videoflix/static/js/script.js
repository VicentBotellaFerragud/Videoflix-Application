const usernameInput = document.getElementById("usernameInput");
const passwordInput = document.getElementById("passwordInput");

const form = document.getElementById("addVideoForm");
const openOrCloseFormButton = document.getElementById("openOrCloseFormbutton");

const titleInput = document.getElementById("titleInput");
const descriptionInput = document.getElementById("descriptionInput");
const videoFileInput = document.getElementById("videoFileInput");
const waitForDiv = document.getElementById("waitForDiv");
const addVideoButton = document.getElementById("addVideoButton");

function openOrCloseForm() {

    form.classList.toggle("hidden");

    const defaultSrc = openOrCloseFormButton.getAttribute("default-src");
    const alternativeSrc = openOrCloseFormButton.getAttribute("alternative-src");

    if (form.className === "add-video-form hidden") {

        addVideoButton.classList.add("transition-none");
        openOrCloseFormButton.setAttribute("src", defaultSrc);

    } else {

        addVideoButton.classList.remove("transition-none");
        openOrCloseFormButton.setAttribute("src", alternativeSrc);

    }

}

function closeMessage() {

    let alertMessages = document.querySelectorAll(".alert");

    for (var i = 0; i < alertMessages.length; i++) {

        alertMessages[i].classList.add("hidden");

    }

}

function displayWaitForDivAndHideAddVideoButton() {

    if (titleInput.value !== "" && descriptionInput.value !== "" && videoFileInput.value !== "") {

        waitForDiv.style.display = waitForDiv.style.display === 'none' ? '' : 'none';
        addVideoButton.style.display = 'none';

    }

}

function checkPasswordValidity() {

    const passwordValue = passwordInput.value;

    const commonPasswords = [
        "123456", "password", "12345678", "1234", "pussy", "12345", "dragon", "qwerty", "696969", "mustang", "letmein", "baseball",
        "master", "michael", "football", "shadow", "monkey", "696969", "mustang", "letmein", "baseball", "master", "michael",
        "football", "shadow", "monkey", "abc123", "pass", "6969", "jordan", "harley", "ranger", "iwantu", "jennifer", "hunter",
        "2000", "test", "batman", "trustno1", "thomas", "tigger", "robert", "access", "love", "buster", "1234567", "soccer", "hockey", 
        "george", "sexy", "andrew", "charlie", "superman", "asshole", "dallas", "jessica", "panties", "pepper", "1111", "austin", 
        "william", "daniel", "golfer", "summer", "heather", "hammer", "yankees", "joshua", "maggie", "biteme", "enter", "ashley",
        "thunder", "cowboy", "silver", "richard", "orange", "merlin", "michelle", "corvette", "bigdog", "cheese", "matthew",
        "121212", "patrick", "martin", "freedom", "ginger", "blowjob", "nicole", "sparky", "yellow", "camaro", "secret", "dick", 
        "falcon", "taylor", "111111", "131313", "123123", "bitch", "hello", "scooter", "please", "porsche", "guitar", "chelsea", 
        "black", "diamond", "nascar", "jackson", "cameron", "654321", "computer", "amanda", "wizard", "xxxxxxxx", "money", "phoenix",
        "mickey", "bailey", "knight", "iceman", "tigers", "purple", "andrea", "horny", "dakota", "aaaaaa", "player", "sunshine", 
        "morgan", "starwars", "boomer", "cowboys", "edward", "charles", "girls", "booboo", "coffee", "xxxxxx", "killer"
    ];

    checkSameAsUsername(passwordValue);
    checkNumberOfCharacters(passwordValue);
    checkNotCommon(passwordValue, commonPasswords);
    checkOnlyNumveric(passwordValue);

}

function checkSameAsUsername(string) {

    if (string.length === 0) {

        condition1.style.visibility = "hidden";

    } else {

        string.includes(usernameInput.value) ? condition1.style.visibility = "hidden" : condition1.style.visibility = "visible";

    }

}

function checkNumberOfCharacters(string) {

    string.length >= 8 ? condition2.style.visibility = "visible" : condition2.style.visibility = "hidden";

}

function checkNotCommon(password, listOfPasswords) {

    if (password.length === 0) {

        condition3.style.visibility = "hidden";

    } else {

        listOfPasswords.includes(password) ? condition3.style.visibility = "hidden" : condition3.style.visibility = "visible";

    }

}

function checkOnlyNumveric(string) {

    if (string.length === 0) {

        condition4.style.visibility = "hidden";

    } else {

        /^\d+$/.test(string) ? condition4.style.visibility = "hidden" : condition4.style.visibility = "visible";

    }

}
