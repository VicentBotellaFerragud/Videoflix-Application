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

    checkNumberOfCharacters(passwordValue);
    checkHasAtLeastOneLetter(passwordValue);
    checkHasAtLeastOneNumber(passwordValue);
    checkContainsAtLeastOneSpecialCharacter(passwordValue);

}

function checkNumberOfCharacters(string) {

    if (string.length >= 10) {

        valid1.style.display = 'block';
        invalid1.style.display = 'none';

    } else {

        valid1.style.display = 'none';
        invalid1.style.display = 'block';

    }

}

function checkHasAtLeastOneLetter(string) {

    if (string.length === 0) {

        valid2.style.display = 'none';
        invalid2.style.display = 'block';

    } else {

        if (/[a-zA-Z]/g.test(string)) {

            valid2.style.display = 'block';
            invalid2.style.display = 'none';

        } else {

            valid2.style.display = 'none';
            invalid2.style.display = 'block';

        }

    }

}

function checkHasAtLeastOneNumber(string) {

    if (string.length === 0) {

        valid3.style.display = 'none';
        invalid3.style.display = 'block';

    } else {

        if (/\d/.test(string)) {

            valid3.style.display = 'block';
            invalid3.style.display = 'none';

        } else {

            valid3.style.display = 'none';
            invalid3.style.display = 'block';

        }

    }

}

function checkContainsAtLeastOneSpecialCharacter(string) {

    const stringAsArray = string.split('');
    const specialCharacters = "[@_!#$%^&*()<>?/|}{~:]";

    if (string.length === 0) {

        valid4.style.display = 'none';
        invalid4.style.display = 'block';

    } else {

        if (stringAsArray.some(char => specialCharacters.includes(char))) {

            valid4.style.display = 'block';
            invalid4.style.display = 'none';

        } else {

            valid4.style.display = 'none';
            invalid4.style.display = 'block';

        }

    }

}
