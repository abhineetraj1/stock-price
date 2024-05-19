if (localStorage.length < 2) {window.location.href="/";}
function logout() {
	localStorage.clear();
	window.location.href="/";
}