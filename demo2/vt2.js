window.onload = function() {
   //luodaan ensin lomake
   var formi = document.getElementById("ruudukko");
   var fieldi = document.createElement("fieldset");
   var p1 = document.createElement("p");
   var p2 = document.createElement("p");
   var p3 = document.createElement("p");
   
   var l1 = document.createElement("label");
   var l2 = document.createElement("label");
   var t1 = document.createTextNode("Leveys ");
   var t2 = document.createTextNode("Pommit ");
   
   l1.appendChild(t1);
   l2.appendChild(t2);
   
   var inp1 = document.createElement("input");
   var inp2 = document.createElement("input");
   var inp3 = document.createElement("input");
   
   inp1.setAttribute("type", "text");
   inp1.setAttribute("name", "x");
   inp1.setAttribute("value", "8");
   
   inp2.setAttribute("type", "text");
   inp2.setAttribute("name", "pommit");
   inp2.setAttribute("value", "4");
   
   inp3.setAttribute("type", "submit");
   inp3.setAttribute("value", "Luo");
   
   p1.appendChild(l1);
   p2.appendChild(l2);
   p1.appendChild(inp1);
   p2.appendChild(inp2);
   p3.appendChild(inp3);
   
   fieldi.appendChild(p1);
   fieldi.appendChild(p2);
   
   formi.appendChild(fieldi);
   formi.appendChild(p3);
   
   inp3.addEventListener("click", tarkista_maarat, false);
   
   muokkaa_tyylit();
}


//lisataan tyylit style-elementtiin
function muokkaa_tyylit() {
   var tyyli = document.getElementsByTagName("style");
   var virhe = document.createTextNode(".virhe {background-color: red;}");
   tyyli[0].appendChild(virhe);
   
   var solu = document.createTextNode("td {margin: 0; padding: 0; border: 0px solid silver;text-align:center;vertical-align: top;background-color: white; min-height: 50px; min-width:50px;}");
   tyyli[0].appendChild(solu);

   var spn = document.createTextNode("span {border: 4px groove silver;min-width: 47px;min-height: 47px;margin: 0;padding: 0;background-color: silver;display: block;}");
   tyyli[0].appendChild(spn);
   
   var img = document.createTextNode("img {margin-top: -10px;padding: 10px;margin-bottom: -15px;min-width: 40px;min-height: 40px;max-width: 40px;}");
   tyyli[0].appendChild(img);
   
   var tyhja = document.createTextNode(".tyhja {border: 4px; min-width: 47px;min-height: 47px;margin: 0;padding: 0;background-color: white;display: block;}");
   tyyli[0].appendChild(tyhja);
}


//syötettyjen arvojen tarkistus
function tarkista_maarat(event) {
   pommien_paikat = new Array();
   event.preventDefault();
   var kentat = document.getElementsByTagName("input");
   var koko = parseInt(kentat[0].value);
   var pommit = parseInt(kentat[1].value);
   
   var epakelpo = 0;

   if (koko < 8 || koko > 32 || isNaN(koko)) {
      kentat[0].setAttribute("class", "virhe");
      epakelpo++;
   }
   else {
      kentat[0].removeAttribute("class");
   }

   if (pommit < 0 || pommit > koko*koko || isNaN(pommit)) {
     kentat[1].setAttribute("class", "virhe");
     epakelpo++;
   }
   else {
      kentat[1].removeAttribute("class");
   }
   
   if (epakelpo == 0) {
      var bodi = document.getElementsByTagName("body")[0];
      //tuhotaan vanha ruudukko
      tuhoa_vanha(bodi);
      //luodaan uusi ruudukko
      luo_uusi(bodi, koko);
      lisaa_pommit(koko, pommit);
   }
}


//tuhotaan jo olemassa oleva taulukko, jos sellainen on
function tuhoa_vanha(vanhempi) {
   var taulu = document.getElementsByTagName("table")[0];
   if (typeof(taulu) == "undefined") return;
   vanhempi.removeChild(taulu);
}


//tehdään tyhjä taulukko, jossa span-elementtejä
function luo_uusi(vanhempi, koko) {
   var taulu = document.createElement("table");
   var tbody =document.createElement('tbody');
   vanhempi.appendChild(taulu);
   taulu.appendChild(tbody);
   var id_luku = 0;
   for (var i=0; i<koko; i++) {
      var rivi = document.createElement("tr");
      for (var j=0; j<koko; j++) {
         var solu = document.createElement("td");
		 solu.setAttribute("id", "t" + id_luku);
		 solu.addEventListener("click", onko_pommi, false);
         var spn = document.createElement("span");
         rivi.appendChild(solu);
         solu.appendChild(spn);
		 id_luku++;
      }
      tbody.appendChild(rivi);
   }
}


//lisätään pommit taulukkoon
function lisaa_pommit(koko, pommit_lkm) {
   //listaan td-elementit, randomisti lkm:n verran ja muutettu pois listasta
   var solut = document.getElementsByTagName("td");
   var i=0;
   while (i<pommit_lkm) {
      var kohta = Math.round(Math.random() * (solut.length - 1));
      console.log(kohta);
	  
      //tutki kuuluuko saatu luku jo käytyihin
	  var poistu = false;
	  for (var j=0; j<pommien_paikat.length; j++) {
		  if (pommien_paikat[j] === kohta) poistu = true;
	  }
	  if (poistu) continue;
	  
	  pommien_paikat[i] = kohta;
	  i++;
   }
}


//tutkitaan, onko klikatussa elementissä pommi
function onko_pommi() {
   var solut = document.getElementsByTagName("td");
   var id = this.getAttribute("id");
   var id_nro = parseInt(id.substring(1));
   
   if(loytyyko_taulukosta(id_nro)) {
	 nayta_pommit(solut);
	 
	 poista_klikkaus(solut);
   }
   else {
	 var muutettava = this.childNodes[0];
	 muutettava.setAttribute("class", "tyhja");
   }
}


//näytetään kaikki pommit taulukossa
function nayta_pommit(elementit) {
   for (var i=0; i<pommien_paikat.length; i++) {
	 var kasiteltava = document.getElementById("t" + pommien_paikat[i]);
	 var poistettava = kasiteltava.childNodes[0];
     kasiteltava.removeChild(poistettava);
     var pommi = document.createElement("img");
     pommi.setAttribute("src", "mine.svg");
     pommi.setAttribute("alt", "pommi");
     pommi.setAttribute("title", "pommi");
	 kasiteltava.appendChild(pommi);
   }
}


//poistetaan tapahtumankäsittelijät
function poista_klikkaus(elementit) {
   for (var i=0; i<elementit.length; i++) {
	 elementit[i].removeEventListener("click", onko_pommi, false);
   }
}


//tutkitaan. löytyykö tietty luku pommien_paikat -taulukosta
function loytyyko_taulukosta(luku) {
   for (var i=0; i<pommien_paikat.length; i++) {
	 if (pommien_paikat[i] === luku) return true;
   }
   return false;
}