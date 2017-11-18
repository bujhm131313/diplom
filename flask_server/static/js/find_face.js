window.onload = function () {
    var example = document.getElementById("coordinates");
    ctx = example.getContext('2d');
    pic = new Image();
    pic.src = img_url;
    pic.onload = function () {
        ctx.drawImage(pic, 0, 0);
    };
};