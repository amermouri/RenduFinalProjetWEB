function RessourceMatiere(m,a){
	
	
$.ajax({
		url:'/download/'+a+'/'+m,
		type: 'GET',
		dataType: 'json',
		
		success: function(data){
			if(data == ''){
				document.getElementById('ressource').innerHTML = "Pas de fichier";
			}else{
				var results= document.getElementById('ressource');
				results.innerHTML= "";
				
				for(d in data){
					console.log(d);
					var html = '<br><div class="row"><a href="uploads/' + data[d]['name']+'" ><font color="FFFFFF"><h3>'+data[d]['name']+'</h3></font></a></div>'
					results.innerHTML += html; 
				}
			}
		}
		
	});

		
}
