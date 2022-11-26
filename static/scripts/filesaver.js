// Saves generated ideas

// Get data from the textarea
const textarea = document.querySelector("textarea"),
// Get file name from the html input
fileNameInput = document.querySelector(".file-name input"),
// Get file extension from the html option
selectMenu = document.querySelector(".save-as select"),
// Set save button to variable
saveBtn = document.querySelector(".save-btn");
// Keep track changes of the file extensions option
selectMenu.addEventListener("change", () => {
    const selectedFormat = selectMenu.options[selectMenu.selectedIndex].text;
    // Change button text to file extension
    saveBtn.innerText = `Save As ${selectedFormat.split(" ")[0]} File`;
});
// Keep track click event of the save button and finally save the file
saveBtn.addEventListener("click", () => {
    const blob = new Blob([textarea.value], {type: selectMenu.value});
    const fileUrl = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.download = fileNameInput.value;
    link.href = fileUrl;
    link.click();
});