window.onload = function () {

    // Find canvas
    var c=document.getElementById("face_square");
    var ctx=c.getContext("2d");

    // coordinates comes from the outer js
    var coors = coordinates;
    c.height = coors[0][2] + coors[0][0];
    c.width = coors[0][3] + coors[0][1];

    var x = coors[0][3];
    var y = coors[0][0];

    var height = coors[0][2] - coors[0][0];
    var width = coors[0][1] - coors[0][3];

    ctx.strokeStyle="#FF0000";
    ctx.rect(x, y, width, height);

    ctx.stroke();
};

