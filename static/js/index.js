
function loginResult() {
	  var login = $('#login').val();
	  var motDePasse = $('#motDePasse').val();
	  
	  
	  $.ajax({
		type:"POST",
		url: "/login",        
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		data: JSON.stringify({
			login: login,
			motDePasse: motDePasse
		}),
		success: function(data){
			if (data['success']) { 
				console.log(data['token']);
				if (typeof(Storage) != "undefined") {
					localStorage.setItem("token", data['token']);
					document.location.href="accueil.html" ;
				} else {
					document.getElementById("result").innerHTML = "Sorry, your browser does not support Web Storage...";
				}
			}
			else {
				alert(data['result']);
			}	
		},
		error:function(){
			alert("Login ou mot de passe incorrect.");
		},
		default: function(){
			alert("Defaut");
		}             
	});
} 

window.onload=function(){

var tok=localStorage.getItem("token");
if (!(tok === null)) {
	$.ajax({
		type:"POST",
		url: "/validate",
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		data: JSON.stringify({
			token : tok
		}),
		success: function(data){
			if (data['success']) {
				document.location.href="accueil.html";
			}
		}
	});
}

}

function runScript(e) {
if (e.keyCode == 13) {
	loginResult();
	return false;
}
}
