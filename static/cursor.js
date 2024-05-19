var cursor = document.createElement("div");
cursor.style = "position:fixed;width:10px;height:10px;border:none;box-shadow:0px 0px 10px black;border-radius:200px;background:black;";
document.body.appendChild(cursor);
document.body.onmousemove = function (e) {
	console.log("s");
	cursor.style.left=e.x+"px";
	cursor.style.top=e.y+"px";
}