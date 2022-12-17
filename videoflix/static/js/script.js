const passwordInput = document.getElementById("passwordInput1");

const titleInput = document.getElementById("titleInput");
const descriptionInput = document.getElementById("descriptionInput");
const videoFileInput = document.getElementById("videoFileInput");
const loadingBar = document.getElementById("loadingBar");
const addVideoButton = document.getElementById("addVideoButton");

function closeMessage() {
    let alertMessages = document.querySelectorAll(".alert");

    for (var i = 0; i < alertMessages.length; i++) {
        alertMessages[i].classList.add("hidden");
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

function searchForVideos() {
    let input, filter, container, videoTitles;

    input = document.getElementById('searchBar');
    filter = input.value.toUpperCase();
    container = document.getElementById('videosWrapper');
    videoTitles = container.querySelectorAll('.video-title');

    for (i = 0; i < videoTitles.length; i++) {
        let videoTitle = videoTitles[i];
        let videoContainer = videoTitle.parentNode.parentNode.parentNode;
        let videoTitleFirstOption = videoTitle.innerHTML;
        let videoTitleSecondOption = videoTitle.innerText;

        videoTitleFirstOption.toUpperCase().indexOf(filter) > -1 ||
            videoTitleSecondOption.toUpperCase().indexOf(filter) > -1 ?
            videoContainer.style.display = 'block' :
            videoContainer.style.display = 'none';
    }
}

function displayLoadingBarAndHideAddVideoButton() {
    if (titleInput.value !== "" && descriptionInput.value !== "" && videoFileInput.value !== "") {
        loadingBar.style.display = loadingBar.style.display === 'none' ? '' : 'none';
        addVideoButton.style.display = 'none';
    }
}

function applyColorToCorrespondingStars(star) {
    const starId = Number(star.id.slice(-1));
    for (let i = starId; i > 0; i--) {
        const star = document.getElementById(`star${i}`);
        star.style.color = 'orange';
    }
}

function removeColorFromAllStars() {
    for (let i = 1; i <= 5; i++) {
        const star = document.getElementById(`star${i}`);
        star.style.color = 'white';
    }
}

function removeMouseAttributesFromAllStars() {
    for (let i = 1; i <= 5; i++) {
        const star = document.getElementById(`star${i}`);
        star.removeAttribute('onmouseover');
        star.removeAttribute('onmouseout');
    }
}

function applyPermanentColor(star) {
    removeMouseAttributesFromAllStars();
    applyColorToCorrespondingStars(star);
    removeColorFromCorrespondingStars(star);
}

function removeColorFromCorrespondingStars(star) {
    const starId = Number(star.id.slice(-1));
    for (let i = starId + 1; i <= 5; i++) {
        const star = document.getElementById(`star${i}`);
        star.style.color = 'white';
    }
}
