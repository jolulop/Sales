function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablink" and remove the background color
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].style.backgroundColor = "";
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.style.backgroundColor = "#ddd";
}

// Open the default tab by simulating a click
document.addEventListener("DOMContentLoaded", function() {
    document.getElementsByClassName("tablink")[0].click();
});

function fetchTime() {
    fetch('https://sales-flaskapp.azurewebsites.net/time')
        .then(response => response.json())
        .then(data => {
            document.getElementById('timeBox').value = data.time;
        })
        .catch(error => console.error('Error fetching time:', error));
}
