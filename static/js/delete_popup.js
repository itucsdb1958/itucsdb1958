function delete_popup() {
    var txt;
    var r = confirm("The element is going to be deleted permanently!");
    if (r == true) {
        document.getElementById("DeleteLink").click();
    } else {
        txt = "You pressed Cancel!";
    }
}