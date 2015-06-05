var err=0;

function signUpResult() {
	
  var login    		 = $('#login').val();
  var nom      		 = $('#nom').val();
  var prenom 		 = $('#prenom').val();
  var annee 		 = $('#annee').val(); 
  var mail     	 	 = $('#mail').val();
  var motDePasse     = $('#motDePasse').val();
  var date_naissance = $('#date_naissance').val(); 
  
  if(login=='' || nom==''|| prenom=='' || annee=='' || mail=='' || motDePasse=='' || date_naissance==''){
	   
	   document.getElementById("generalError").innerHTML ='<div class="alert alert-error"><a href="#" class="close" data-dismiss="alert">&times;</a>Tu dois remplir tous les champs !</div>';
	
	}else if(err > 0){
	
	document.getElementById("generalError").innerHTML ='<div class="alert alert-error"><a href="#" class="close" data-dismiss="alert">&times;</a>Tu dois fournir des formats valides !</div>';
	
	}else{
   
	  $.ajax({
		type:"POST",
		url: "/signUp",        
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		data: JSON.stringify({
			login: login,
			nom: nom,
			prenom: prenom,
			annee: annee,
			mail: mail,
			motDePasse: motDePasse,
			date_naissance: date_naissance
		}),
		success: function(data){
			if ( data['success']) { 
				console.log(data['token']);
				if (typeof(Storage) != "undefined") {
					localStorage.setItem("token", data['token']);
					document.location.href="accueil.html" ;
				} else {
					document.getElementById("result").innerHTML = "Ton navigateur ne supporte pas le Web Storage.";
				}
			}
			else {
				document.getElementById("generalError").innerHTML ='<div class="alert alert-error"><a href="#" class="close" data-dismiss="alert">&times;</a>Ton login est déjà pris !</div>';

			}	
		},
		error:function(){
			alert("Login ou mot de passe incorrect.");
		},
		timeout: 3000              
	
	});
}
}

function surligne(champ, erreur)
{
   if(erreur)
      champ.style.backgroundColor = "#fba";
   else
      champ.style.backgroundColor = "";
}

function validateLogin(champ)
{
   if(champ.value.length < 3 || champ.value.length > 20)
   {
   	  err++;
      document.getElementById("loginError").innerHTML ='<div class="alert alert-error"><a href="#" class="close" data-dismiss="alert">&times;</a>Ton login doit avoir une longueur comprise entre 3 et 20 caractères !</div>'
      surligne(champ, true);
      return false;
   }
   else
   {
  	  err--;
      document.getElementById("loginError").innerHTML =''
      surligne(champ, false);
      return true;
   }
}

function validateMail(champ)
{
   var regex = /^[a-zA-Z0-9._-]+@[a-z0-9._-]{2,}\.[a-z]{2,4}$/;
   if(!regex.test(champ.value))
   {
   	  err++;
   	  document.getElementById("mailError").innerHTML ='<div class="alert alert-error"><a href="#" class="close" data-dismiss="alert">&times;</a>Format du mail invalide !</div>'
      surligne(champ, true);
      return false;
   }
   else
   {
  	  err--;
      document.getElementById("mailError").innerHTML =''
      surligne(champ, false);
      return true;
   }
}



function validateDate(champ){
  if (champ.match(/^(0[1-9]|[12][0-9]|3[01])[\- \/.](?:(0[1-9]|1[012])[\- \/.](19|20)[0-9]{2})$/)){
  	err--;
  	document.getElementById("dateError").innerHTML ='<div class="alert alert-error"><a href="#" class="close" data-dismiss="alert">&times;</a>Format de la date invalide !</div>'
    surligne(champ, true);
    return true;
  }else{
   	err++;
  	document.getElementById("dateError").innerHTML =''
    surligne(champ, false);
    return false;
  }
}
