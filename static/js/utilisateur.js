window.onload=function(){
	var login;
	var tok=localStorage.getItem("token");
	
	$.ajax({
		type:"POST",
		url: "/users",        
		dataType: "json",
		contentType: "application/json; charset=utf-8",
		data: JSON.stringify({
			Token: tok,
		}),
		success: function(data){
			login=data['username'];
			var Codehtml = ' <a>Connecté en tant que '+data['username']+'</a>';		
			console.log(Codehtml);
			var results= document.getElementById('UserLogMenu');
			results.innerHTML += Codehtml;
		},
		error:function(){
			alert("Tu dois te connecter !");
			document.location.href="index.html"
		},
		default: function(){
			alert("Defaut");
			document.location.href="index.html"
		}             
	});
		
	$.ajax({
			type:"POST",
            url: "/profile",        
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
				Token: tok
			}),
			success: function(data){
				var html='<br><div><h3> Tes infos</h3><ul><li><strong>Prénom : </strong>' +data['prenom']+'</li><li><strong>Nom : </strong>'+ data['nom']+'</li><li><strong>Année : </strong>' +data['annee']+'</li> <li><strong>Mail : </strong>'+data['mail']+'</li> <li><strong>Date anniversaire : </strong>'+ data['date_naissance']+'</li></ul></div>'
				var results= document.getElementById('profile');
				results.innerHTML += html;  
				mail = data['mail'];
				annee = data['annee'];
			},
			error:function(){
				Deconnexion();
			},
			default: function(){
				Deconnexion();
			}         
		});
}
