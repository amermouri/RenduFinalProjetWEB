 
 
 function add_ressource(){
 
	//DATA
	var $nom_fich = $('#nomFichier').val();
	var $annee_fich = $('#annee').val();
	var $cours_fich = $('#matiere').val();
	var $type_fich = $('#typeRessource').val();
	
	
	/***** ENVOI CORRECT *****/
	$.ajax({
	 
		type: 'POST',
		url: '/upload',
		dataType : 'json',
		data: {year:$annee_fich, course:$cours_fich, type:$type_fich},
		success: toto,
		error:function(){
			alert("Erreur");
		}
		
	});
	
}

var toto = function(data){
   $('#llh').val(data['ll']);
   $('#mmh').val(data['mm']);
   $('#pph').val(data['pp']);
}
