// image file size checker by creating a cookie

function filesize(elem){


    document.cookie = `"filesize=${elem.files[0].size}"`;


}


function imageAlert() {
    alert("Image Saved");
}