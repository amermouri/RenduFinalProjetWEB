
function Deconnexion(){
	localStorage.removeItem("token");
	document.location.href = "index.html";
}
