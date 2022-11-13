//Global variables:
const form = document.getElementById("addVideoForm");
const openOrCloseFormButton = document.getElementById("openOrCloseFormbutton");
const DefaultSrc = openOrCloseFormButton.getAttribute("default-src");
const AlternativeSrc = openOrCloseFormButton.getAttribute("alternative-src");
const addVideoButton = document.getElementById("addVideoButton");

function openOrCloseForm() {

    form.classList.toggle("hidden");
    
    if (form.className === "add-video-form hidden") {

        addVideoButton.classList.add("remove-transition");
        openOrCloseFormButton.setAttribute("src", DefaultSrc);

    } else {

        addVideoButton.classList.remove("remove-transition");
        openOrCloseFormButton.setAttribute("src", AlternativeSrc);

    }

}
