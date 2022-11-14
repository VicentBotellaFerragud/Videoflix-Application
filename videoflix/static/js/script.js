//Global variables:
const form = document.getElementById("addVideoForm");
const openOrCloseFormButton = document.getElementById("openOrCloseFormbutton");
const DefaultSrc = openOrCloseFormButton.getAttribute("default-src");
const AlternativeSrc = openOrCloseFormButton.getAttribute("alternative-src");
const addVideoButton = document.getElementById("addVideoButton");

/**
 * Displays/hides the "addVideoForm" and makes some small style changes in some elements of the home page depending on the state of 
 * the form (if it's visible or not).
 */
function openOrCloseForm() {

    form.classList.toggle("hidden");
    
    if (form.className === "add-video-form hidden") {

        addVideoButton.classList.add("transition-none");
        openOrCloseFormButton.setAttribute("src", DefaultSrc);

    } else {

        addVideoButton.classList.remove("transition-none");
        openOrCloseFormButton.setAttribute("src", AlternativeSrc);

    }

}
