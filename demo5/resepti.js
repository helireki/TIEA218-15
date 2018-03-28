//ikkunan latauksen yhteydessä
window.onload = function() {
  hae_reseptit();
  hae_ruokalajit();
  $('#lisaa').on("click", lisaa_resepti_kantaan);
  
  $('#nimi').on("change", tarkista_nimi);
  $('#hlo').on("change", tarkista_hlo);
  
  $("#ei").attr("class", "hidden");
  $("#onnistui").attr("class", "hidden");
  
  $("#lisaa").attr("disabled", "disabled");
  $('#nimis').attr("class", "hidden");
  $('#hlos').attr("class", "hidden");
  $('#nimi').val("");
  $('#kuvaus').val("");
  $('#hlo').val("");
  //tyhjennetään vaihelista
  var vaiheet = $('.vaihe');
  for (i=0; i<vaiheet.length; i++) {
	  $(vaiheet[i]).val("");
  }
  
  $('#valitse').on("click", hae_valinta);
  $('#muok_onnistui').attr("class", "hidden");
  $('#muok_ei').attr("class", "hidden");
}


//valmistaudutaan joko ruokalajin lisäämiseen tai muokkaamiseen
function hae_valinta() {
  var valittu = $('#list2').val();
  $('#tiedot').empty();
  if (valittu == '0') {
    //tehdään uuden lisäyslomake
	var h2 = document.createElement("h2");
    var teksti = "Uuden ruokalajin lisääminen:";
    var textnode = document.createTextNode(teksti);
    h2.appendChild(textnode);
    $('#tiedot').append(h2);
    var h3 = document.createElement("h3");
    teksti = "Uusi ruokalaji";
    textnode = document.createTextNode(teksti);
    h3.appendChild(textnode);
	h3.tunniste = "0";
	h3.setAttribute("id", "muok_tai_lis");
    $('#tiedot').append(h3);
    tee_kenttalomake();
	$('#laheta').attr("disabled", "disabled");
  }
  else {
    //tehdään ruokalajin tietojen haku ja lomake
	$.ajax({
	  async: true,
	  url: "hae_ruokalaji.py",
	  data: {"valittu":valittu},
	  dataType: "json",
	  type: "GET",
	  success: nayta_ruokalaji,
	  error: ajax_virhe
	});
  }
  $('#ruoka_viesti').attr("class", "hidden");
}


//laitetaan ruokalajin kannasta haetut tiedot näkyviin
function nayta_ruokalaji(data) {
	var h2 = document.createElement("h2");
    var teksti = "Ruokalajin tietojen muokkaaminen:";
    var textnode = document.createTextNode(teksti);
    h2.appendChild(textnode);
    $('#tiedot').append(h2);
    textnode = document.createTextNode(data["nimi"]);
	var ot = document.createElement("h3");
    ot.appendChild(textnode);
	ot.tunniste = data["id"];
	ot.setAttribute("id", "muok_tai_lis");
    $('#tiedot').append(ot);
	tee_kenttalomake();
	//tietojen paikoilleen asettaminen
	$('#nimi_ruoka').val(data["nimi"]);
	$('#kuvaus_ruoka').val(data["kuvaus"]);
	
}


//tehdään kenttä ruokalajin käsittelylle
function tee_kenttalomake() {
  //tässä tehdään formi pohjaksi
  var formi = document.createElement("form");
  formi.setAttribute("method", "post");
  
  var p1 = document.createElement("p");
  var p2 = document.createElement("p");
  
  var i1 = document.createElement("input");
  i1.setAttribute("type", "text");
  i1.setAttribute("name", "nimi");
  i1.setAttribute("id", "nimi_ruoka");
  var l1 = document.createElement("label");
  l1.setAttribute("for", "nimi_ruoka");
  var t1 = document.createTextNode("Ruokalajin nimi ");
  l1.appendChild(t1);
  p1.appendChild(l1);
  p1.appendChild(i1);
  
  var span = document.createElement("span");
  span.appendChild(document.createTextNode(" Ruokalajin nimi ei saa olla tyhjä."));
  p1.appendChild(span);
  span.setAttribute("id", "nimi_r");
  span.setAttribute("class", "hidden");

  var i2 = document.createElement("input");
  i2.setAttribute("type", "text");
  i2.setAttribute("name", "kuvaus");
  i2.setAttribute("id", "kuvaus_ruoka");
  var l2 = document.createElement("label");
  l2.setAttribute("for", "kuvaus_ruoka");
  t2 = document.createTextNode("Ruokalajin kuvaus ");
  l2.appendChild(t2);
  p2.appendChild(l2);
  p2.appendChild(i2);

  formi.appendChild(p1);
  formi.appendChild(p2);

  var subinp = document.createElement("input");
  subinp.setAttribute("type", "button");
  var teksti = "Lähetä";
  subinp.setAttribute("value", teksti);
  subinp.setAttribute("id", "laheta");
  
  var p3 = document.createElement("p");
  p3.appendChild(subinp);
  
  formi.appendChild(p3);
  $('#tiedot').append(formi);
  
  //lisätään käsittelijä virheilmoituksille ja lähetä-nappulalle
  $('#nimi_ruoka').on("change", function() {
    var nimir = document.getElementById("nimi_r");
    if ($(this).val() == "") {
	  nimir.removeAttribute("class");
	  $('#laheta').attr("disabled", "disabled");
	  return;
    }
    nimir.setAttribute("class", "hidden");
	$('#laheta').removeAttr("disabled");
  });
  
  $('#laheta').on("click", lisaa_ruokalaji_kantaan);
}


//ajax-kutsu, jossa lisätään ruokalaji kantaan
function lisaa_ruokalaji_kantaan() {
  var ruoka = document.getElementById("muok_tai_lis");
  $.ajax({
    async: true,
	url: "lisaa_ruokalaji_kantaan.py",
	data: {"id":ruoka.tunniste, "nimi":$('#nimi_ruoka').val(), "kuvaus":$('#kuvaus_ruoka').val()},
	dataType: "text",
	success: ruokalaji_onnistui,
	error: ajax_virhe
});
}


//mitä tehdään, jos ruokalajin lisäys/muokkaus onnistui
function ruokalaji_onnistui(data, textStatus, request) {
  var vanh = $("#ruoka_viesti");
  var nimi = "";
  var viesti = "";
  var ruoka = $("#muok_tai_lis");
  if (data == '1') {
    viesti = "Muokkaus onnistui!";
	nimi = $('#nimi_ruoka').val();
    ruoka.empty();
    ruoka.append(document.createTextNode(nimi));
  }
  if (data == '-2') {
    viesti = "Virhe ruokalajin muokkauksessa.";
  }
  if (data == '0') {
    viesti = "Lisäys onnistui!";
	$('#nimi_ruoka').val("");
	$('#kuvaus_ruoka').val("");
	ruoka.empty();
  }
  if (data == '-1') {
    viesti = "Virhe ruokalajin lisäyksessä.";
	$('#nimi_ruoka').val("");
	$('#kuvaus_ruoka').val("");
  }
  vanh.empty();
  vanh.append(document.createTextNode(viesti));
  vanh.removeAttr("class");
  hae_ruokalajit();
}


//ajax-kutsu, jossa lisätään uusi resepti kantaan
function lisaa_resepti_kantaan() {
  $.ajax({ 
    async: true,
    url: "lisaa_resepti_kantaan.py", 
    data: {"nimi": $('#nimi').val(), "kuvaus":$('#kuvaus').val(), "hlo":$('#hlo').val(), "ruoka":$('#list').val(),
	      "vaihe1":$('#vaihe1').val(), "vaihe2":$('#vaihe2').val(), "vaihe3":$('#vaihe3').val(), "vaihe4":$('#vaihe4').val(),
		  "vaihe5":$('#vaihe5').val(), "vaihe6":$('#vaihe6').val(), "vaihe7":$('#vaihe7').val(), "vaihe8":$('#vaihe8').val(),
		  "vaihe9":$('#vaihe9').val(), "vaihe10":$('#vaihe10').val()},
    dataType: "text",
    type: "GET",
    success: lisays_onnistui,
    error: ajax_virhe
  });
}


//tarkistetaan reseptin lisäämiseen liittyvistä kentistä tulleet virheet
function tarkista_virheet() {
  if ($('#nimi').val() == "" || $('#hlo').val() == "") {
    $('#lisaa').attr("disabled", "disabled");
	return;
  }
  /*var spanit = $('span');
  for(i=0; i<2;i++) {
    if ( $(spanit[i]).attr("class") != "hidden" ) {
      $('#lisaa').attr("disabled", "disabled");
	    return;
      }
  }*/
  if ($('#nimis').attr("class") != "hidden" || $('#hlos').attr("class") != "hidden") {
    $('#lisaa').attr("disabled", "disabled");
  }
  $('#lisaa').removeAttr("disabled");
}


//tarkistetaan, onko uuden reseptin nimi oikein
function tarkista_nimi() {
  var nimis = document.getElementById("nimis");
  if ($(this).val() == "") {
	nimis.removeAttribute("class");
	$('#lisaa').attr("disabled", "disabled");
	return;
  }
  nimis.setAttribute("class", "hidden");
  tarkista_virheet();
}


//tarkistetaan, onko uuden reseptin nimi oikein
function tarkista_hlo() {
  var hlos = document.getElementById("hlos");
  var arvo = parseInt($(this).val());
  if (arvo < 1 || isNaN(arvo)) {
    hlos.removeAttribute("class");
	$('#lisaa').attr("disabled", "disabled");
    return;
  }
  hlos.setAttribute("class", "hidden");
  tarkista_virheet();
}


//mitä tehdään, kun uuden reseptin lisääminen onnistui
function lisays_onnistui(data, textStatus, request) {
  var bodi = document.getElementById("bodi");
  viesti = ""
  if (data == "0") {
    $("#onnistui").removeAttr("class");
    $("#nimi").val("");
    $("#kuvaus").val("");
    $("#hlo").val("");
	$("#lisaa").attr("disabled", "disabled");
	//täällä voisi myös tyhjentää vaiheet
	var vaiheet = $('.vaihe');
    for (i=0; i<vaiheet.length; i++) {
	  $(vaiheet[i]).val("");
    }
  }
  else {
    $("#ei").removeAttr("class");
  }
  hae_reseptit();
}


//ajax-kutsu, jossa haetaan kaikki reseptit
function hae_reseptit() {
  $.ajax({
    async: true,
    url: "hae_reseptit.py",
    processData: true,
    dataType: "json",
    type: "GET",
    success: lisaa_reseptit,
    error: ajax_virhe
  });
}


//mitä tehdään, kun reseptien haku onnistui
function lisaa_reseptit(data) {
  var lista = $('#reseptilistaus');
  lista.empty();
  //data on kaksiulotteisessa taulukossa
  var edellinen = 0;
  var ohjelista = "";
  $.each(data, function(key, val) {
    var id = val[0];
	if (id != edellinen) {
      //luodaan ulkolistaan vaihe
	  var alkio = document.createElement("li");
	  //omien tunnisteiden luominen on mahdollista
      alkio.tunniste = val[0];
      alkio.appendChild(document.createTextNode(val[1]));
      lista.append(alkio); //lista jquery-objekti, jqueryn funktio
	  alkio.setAttribute("class", "ulko");
	  $(alkio).on("click", muokkaa_reseptia);
	}
	if (val[2] != null) {
	  if (id != edellinen) {
	    //luodaan uusi sisälista
		var li = document.createElement("li");
		var sisalista = document.createElement("ol");
		li.appendChild(sisalista);
		li.setAttribute("class", "ulko_eka");
		//ja sinne alkio
		li2 = document.createElement("li");
		li2.appendChild(document.createTextNode(val[2]));
		sisalista.appendChild(li2);
		lista.append(li);
		edellinen = id;
		ohjelista = sisalista;
	  }
	  else {
	    //luodaan vain sisäalkio
		var vaihealkio = document.createElement("li");
	    vaihealkio.appendChild(document.createTextNode(val[2]));
	    //sisempään listaan lisäys vielä
		ohjelista.appendChild(vaihealkio);
	  }
	}
	else {
      return true;
	}	
  });
}


//lomake, jolla on mahdollista muokata valittua reseptiä
function muokkaa_reseptia() {
  //näytetään muokkausta varten lomake
  var lapset = $('#muok_oikea').children();
  for (i=0;i<lapset.length;i++) {
    $(lapset[i]).removeAttr("class", "hidden");
  }
  $('#muok_nimis').attr("class", "hidden");
  $('#muok_hlos').attr("class", "hidden");
  $('#muok_onnistui').attr("class", "hidden");
  $('#muok_ei').attr("class", "hidden");
  
  $('#tallenna').on("click", lisaa_muokkaukset_kantaan);
  
  hae_ruokalajit();
  //haetaan tunnisteen perusteella reseptin tiedot
  $.ajax({
    async: true,
    url: "hae_resepti.py",
    data: {"id":this.tunniste},
    processData: true,
    dataType: "json",
    type: "GET",
    success: lisaa_tiedot,
    error: ajax_virhe
  });
}


//ajax-kutsu, jossa lisätään reseptin muokkaukset kantaan
function lisaa_muokkaukset_kantaan() {
  var otsikko = document.getElementById("res_otsikko");
  $.ajax({
    async: true,
    url: "lisaa_muokkaukset_kantaan.py",
    data: {"id":otsikko.tunniste, "nimi":$('#muok_nimi').val(), "kuvaus":$('#muok_kuvaus').val(), "hlo":$('#muok_hlo').val(),
          "ruokaid":$('#list3').val(), "vaihe1":$('#muok_vaihe1').val(), "vaihe2":$('#muok_vaihe2').val(), "vaihe3":$('#muok_vaihe3').val(),
          "vaihe4":$('#muok_vaihe4').val(), "vaihe5":$('#muok_vaihe5').val(), "vaihe6":$('#muok_vaihe6').val(), "vaihe7":$('#muok_vaihe7').val(),
          "vaihe8":$('#muok_vaihe8').val(), "vaihe9":$('#muok_vaihe9').val(), "vaihe10":$('#muok_vaihe10').val()},
    processData: true,
    dataType: "text",
    type: "GET",
    success: reseptin_muokkaus_onnistui,
    error: ajax_virhe
  });
}


//mitä tehdään, kun reseptin muokkaus onnistui
function reseptin_muokkaus_onnistui(data, textStatus, request) {
  if (data == "-1" || data == "-10") {
    $('#muok_ei').removeAttr("class", "hidden");
    $('#muok_onnistui').attr("class", "hidden");
  }
  else {
    $('#muok_ei').attr("class", "hidden");
    $('#muok_onnistui').removeAttr("class", "hidden");
    
    //vaiheiden, jotka eivät menneet kantaan, poisto näkyvistä
    var ot = document.getElementById("res_otsikko");
    $.ajax({
      async: true,
      url: "hae_resepti.py",
      data: {"id":ot.tunniste},
      processData: true,
      dataType: "json",
      type: "GET",
      success: nayta_uudet_tiedot,
      error: ajax_virhe
    });
  }
  hae_reseptit();
}


//näytetään reseptin uudet tiedot
function nayta_uudet_tiedot(data) {
  nayta_tiedot(data, 1);
}


//näytetään valitun reseptin tiedot
function nayta_tiedot(data, arvo) {
  nimi = "";
  kuvaus = "";
  hlomaara = "";
  ruokaid = "";
  ohjeet = [];
  id = 0;
  
  $.each(data, function(key, val) {
    if (nimi == "") {
      id = val[0];
      nimi = val[1];
      kuvaus = val[2];
      hlomaara = val[3];
      ruokaid = val[4];
    }
    if (val[4] != null) ohjeet.push(val[5]);
  });
  $('#res_otsikko').empty();
  $('#res_otsikko').append(document.createTextNode(nimi));
  var ot = document.getElementById("res_otsikko");
  ot.tunniste = id;
  
  $('#muok_nimi').val(nimi);
  $('#muok_kuvaus').val(kuvaus);
  $('#muok_hlo').val(hlomaara);
  if (arvo == 0) {
    //lisätään myös tapahtumankäsittelijät tiedon oikeellisuudelle, kun tullaan 1. kerran
    $('#muok_nimi').on("change", tarkista_uusi_nimi);
    $('#muok_hlo').on("change", tarkista_uusi_hlo);
  }
  
  var optionit = $('#list3').children("option");
  for (i=0;i<optionit.length;i++) {
    if ($(optionit[i]).val() == ruokaid) {
       $(optionit[i]).attr("selected", "selected");
       break;
    }
  }
  for (i=0;i<10;i++) {
    $('#muok_vaihe' + (i+1)).val("");
  }
  nayta_ohjeet(ohjeet);
}
 
 
 //näytetään reseptin tiedot 1. kertaa lomakkeella
function lisaa_tiedot(data) { 
  nayta_tiedot(data, 0);
}


//tarkistetaan, onko reseptin muokkaukseen liittyvistä kentistä tullut virheitä
function tarkista_muok_virheet() {
  if ($('#muok_nimi').val() == "" || $('#muok_hlo').val() == "") {
    $('#tallenna').attr("disabled", "disabled");
	return;
  }
  if ($('#muok_nimis').attr("class") != "hidden" || $('#muok_hlos').attr("class") != "hidden") {
    $('#tallenna').attr("disabled", "disabled");
  }
  $('#tallenna').removeAttr("disabled");
}


//tarkistetaan, että reseptin uusi nimi on oikein
function tarkista_uusi_nimi() {
  var nimis = document.getElementById("muok_nimis");
  if ($(this).val() == "") {
	nimis.removeAttribute("class");
	$('#tallenna').attr("disabled", "disabled");
	return;
  }
  nimis.setAttribute("class", "hidden");
  tarkista_muok_virheet();
}


//tarkistetaan ,että reseptin uusi nimi on oikein
function tarkista_uusi_hlo() {
  var hlos = document.getElementById("muok_hlos");
  var arvo = parseInt($(this).val());
  if (arvo < 1 || isNaN(arvo)) {
    hlos.removeAttribute("class");
	$('#tallenna').attr("disabled", "disabled");
    return;
  }
  hlos.setAttribute("class", "hidden");
  tarkista_muok_virheet();
}


//näytetään reseptiin kuuluvat ohjeet
function nayta_ohjeet(ohjeet) {
  for (i=0;i<ohjeet.length;i++) {
    $('#muok_vaihe' + (i+1)).val(ohjeet[i]);
  }
}


//ajax-kutsu, jolla haetaan ruokalajit kannasta
function hae_ruokalajit() {
  $.ajax({
    async: true,
    url: "hae_ruokalajit.py",
    processData: true,
    dataType: "json",
    type: "GET",
    success: lisaa_ruokalajit,
    error: ajax_virhe
  });
}


//mitä tehdään, kun ruokalajien haku onnistui
function lisaa_ruokalajit(data, textStatus, request) {
  var select = $('#list');
  select.empty();
  var toinen_select = $('#list2');
  toinen_select.empty();
  var eka_valinta = document.createElement("option");
  eka_valinta.setAttribute("value", 0);
  eka_valinta.appendChild(document.createTextNode("Lisää uusi ruokalaji"));
  toinen_select.append(eka_valinta);
  eka_valinta.setAttribute("selected", "selected");
  
  var kolmas_select = $('#list3');
  //jos valittu joku option, otetaan sen id talteen ja laitetaan uudelleen valituksi myöhemmin
  var valittu = $(kolmas_select).children(':selected');
  var valittu_arvo = -1;
  if (valittu !== 'undefined') {
    valittu_arvo = $(valittu).val();
  }
  kolmas_select.empty();
  
  $.each(data, function(key, val) {
    var alkio = document.createElement("option");
	var alkio2 = document.createElement("option");
    var alkio3 = document.createElement("option");
    alkio.setAttribute("value", key);
	alkio2.setAttribute("value", key);
    alkio3.setAttribute("value", key);
    alkio.appendChild(document.createTextNode(val));
	alkio2.appendChild(document.createTextNode(val));
    alkio3.appendChild(document.createTextNode(val));
    if (valittu_arvo == key) {
      alkio3.setAttribute("selected", "selected");
    }
    select.append(alkio); //select jquery-objekti, jqueryn funktio	
	toinen_select.append(alkio2);
    kolmas_select.append(alkio3);
  });
  // select[0] palauttaa jquery-objektista varsinaisen dom-objektin
  select[0].firstChild.setAttribute("selected", "selected");
}


//jos ajax-kutsussa tulee ongelmia
function ajax_virhe(event, jqxhr, settings, exception) {
  //täältä voi tulla http:hen liittyviä virheitä
  $('#bodi').append(document.createTextNode(exception));
}