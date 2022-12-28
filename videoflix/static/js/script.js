const categoryInput = document.getElementById("categoryInput");
const titleInput = document.getElementById("titleInput");
const descriptionInput = document.getElementById("descriptionInput");
const videoFileInput = document.getElementById("videoFileInput");
const addVideoButton = document.getElementById("addVideoButton");
const loadingBar = document.getElementById("loadingBar");
const waitInfo = document.getElementById("waitInfo");

$(function () {
    $('[data-toggle="popover"]').popover()
})

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

function closeMessage() {
    let alertMessages = document.querySelectorAll(".alert");

    for (var i = 0; i < alertMessages.length; i++) {
        alertMessages[i].style.display = 'none';
    }
}

function scrollToLeft(videoRow) {
    document.getElementById(`videoRow${videoRow}`).scrollLeft += 1000;
    console.log(document.getElementById(`videoRow${videoRow}`));
}

function scrollToRight(videoRow) {
    document.getElementById(`videoRow${videoRow}`).scrollLeft -= 1000;
}

function displayLoadingBarAndHideAddVideoButton() {
    if (categoryInput.value !== "" && titleInput.value !== "" && descriptionInput.value !== "" && videoFileInput.value !== "") {
        loadingBar.style.display = loadingBar.style.display === 'none' ? '' : 'none';
        waitInfo.style.display = waitInfo.style.display === 'none' ? '' : 'none';
        addVideoButton.style.display = 'none';
    }
}

function searchForVideos(homeOrMyVideos) {
    let input, filter, container, videoTitles;

    input = document.getElementById(`searchBar${homeOrMyVideos}`);
    filter = input.value.toUpperCase();
    container = document.getElementById(`videosWrapper${homeOrMyVideos}`);
    videoTitles = container.querySelectorAll(`.video-title-${homeOrMyVideos}`);

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

function navigateUserToVideoDetailsView(videoPk) {
    window.location.href = `/video-details/${videoPk}`;
}
