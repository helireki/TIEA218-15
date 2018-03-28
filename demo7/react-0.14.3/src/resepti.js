//komponentti, joka käsittelee reseptilistausta ja lomaketta
var Reseptit = React.createClass({
  //komponentin alkutila
  getInitialState: function() {
    return {
      reseptit: [],
      ruokalajit: [],
      aineet: [],
      liittyy: [],
      jarj: "aakkos"
    }
  },
  
  //mitä tehdään, kun komponentti kiinnittyy
  componentDidMount: function() {
    $.get(this.props.source, function(tulos){
      var reseptit = tulos[0];
      var ruokalajit = tulos[1];
      var aineet = tulos[2];
      var liittyy = tulos[3];
      if (this.isMounted()) {
        reseptit = reseptit.map(function(item) {
          return item;
        });
        ruokalajit = ruokalajit.map(function(item) {
          return item;
        });
        aineet = aineet.map(function(item) {
          return item;
        });
        liittyy = liittyy.map(function(item) {
          return item;
        });
        this.setState({reseptit: reseptit, ruokalajit: ruokalajit, aineet: aineet, liittyy: liittyy});
      }
      }.bind(this));
  },
  
  //käännetään reseptilistauksen aakkosjärjstyksen arvo
  kaannaListaus: function () {
    if (this.state.jarj === "aakkos") {
      this.setState({jarj: "kaant"});
    }
    else {
      this.setState({jarj: "aakkos"});
    }
  },
  
  //renderöidään komponentti
  render: function() {
    return (
      <div>
      <div id="vasen">
        <h2>Reseptilistaus</h2>
        <button onClick={this.kaannaListaus}>Käännä listauksen järjestys</button>
        <Lista reseptit={this.state.reseptit} ruokalajit={this.state.ruokalajit} aineet={this.state.aineet} 
        liittyy={this.state.liittyy} jarjestys={this.state.jarj}/>
      </div>
      <div id="oikea">
        <Lomake ruokalajit={this.state.ruokalajit}/>
      </div>
      </div>
    );
  }
});


//reseptilistauksen komponetti
var Lista = React.createClass({
  //järjestetään aakkonjärjestykseen
  laitaAakkosjarjestykseen: function(a,b) {
    if (a.nimi > b.nimi) {
      return 1;
    }
    if (a.nimi < b.nimi) {
      return -1;
    }
    return 0;
  },
  
  //järjestetään käänteiseen järjestykseen
  laitaKaanteiseen: function(a,b) {
    if (a.nimi > b.nimi) {
      return -1;
    }
    if (a.nimi < b.nimi) {
      return 1;
    }
    return 0;
  },
  
  //komponentin renderöinti
  render: function() {
    var self = this;
    var reseptit = this.props.reseptit;
    if (this.props.jarjestys === "aakkos") {
      reseptit = reseptit.sort(this.laitaAakkosjarjestykseen);
    }
    else {
      reseptit = reseptit.sort(this.laitaKaanteiseen);
    }
    return (
      <ul>
      {
        reseptit.map(function(item) {
          //filter palauttaa listan
          var reseptin_ruoka = self.props.ruokalajit.filter(function(item2) {
            return item["ruokalajiID"] == item2.key;
          });
          
          var reseptiin_liittyvat = self.props.liittyy.filter(function(item3) {
            return item.key == item3["reseptiID"];
          });
          return <div>
                 <li key={item.key}>{item.nimi} - {reseptin_ruoka[0].nimi}</li>
                 <li className="ekapoisto">
                   <ul className="sisa">
                     {
                       reseptiin_liittyvat.map(function(liittyva) {
                         var aine = self.props.aineet.filter(function(aine) {
                           return liittyva["aineID"] == aine.key;
                         });
                         return <li>{aine[0].nimi}, {liittyva.maara} {liittyva.yksikko_l}</li> 
                       })
                     }
                   </ul>
                 </li>
                 </div>
        })
      }
      </ul>
    )
  }
});


//lomake reseptin lisäystä varten
var Lomake = React.createClass({
  //komponentin alkutila
  getInitialState: function() {
    return {nimi: "", kuvaus: "", henkilomaara: 0, ruokalaji: "Alkuruoka"};
  },
  
  //lisäyksen käsittely, tässä versiossa ei tee mitään
  kasitteleLisays: function(e) {
    e.preventDefault();
  },
  
  //komponentin renderöinti
  render: function() {
    return (
      <form>
        <h2>Reseptin lisäys</h2>
        <h3>Lisää uusi resepti täyttämällä kentät.</h3>
        <p><label htmlFor="nimi">Nimi </label>
          <input type="text" name="nimi" id="nimi"/>
        </p>
        <p><label htmlFor="kuvaus">Kuvaus </label>
          <input type="text" name="kuvaus" id="kuvaus"/>
        </p>
        <p><label htmlFor="hlo">Henkilömäärä </label>
          <input type="text" name="hlo" id="hlo"/>
        </p>
        <p>
          <label htmlFor="select">Ruokalaji </label><Select id="select" name="ruokalajit" ruokalajit={this.props.ruokalajit}/>
        </p>
        <p><button onClick={this.kasitteleLisays}>Lisää resepti</button></p>
      </form>
    )
  }
});


//select-lista ruokalajin valintaa varten
var Select = React.createClass({
  //komponenti renderöinti
  render: function() {
    var self = this;
    var nro = 0;
    return (
      <select name={this.props.name} defaultValue={self.props.ruokalajit[0]}>
          {
            this.props.ruokalajit.map(function(item) {
              return <option key={nro += 1} value={item.nimi}>{item.nimi}</option>
            })
          }
      </select>
    )
  }
});

//koko dynaamisen osuuden renderöinti, liitetään osaksi main-diviä
ReactDOM.render(
  <div>
    <h1>Reseptit</h1>
    <Reseptit source="http://users.jyu.fi/~helireki/wsovellukset15/demo7/react-0.14.3/src/aineisto.json"/>
  </div>,
  document.getElementById('main'));