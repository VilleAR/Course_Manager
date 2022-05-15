# Course_Manager
Repo tietokantasovellukselle

Käyttäjät voi tehdä vapaasti, käyttäjän tyypin saa valita (oppilas tai opettaja). Sovelluksen käytettävyys vaihtelee
käyttäjän tyypistä riippuen.

Sovellus ei ole kovinkaan hiottu varsinkaan viimeisten lisäysten osalta (courselist), mutta ainakin pikaisella testauksella
vaikuttaa toimivan. Olen keskittynyt enimmäkseen ominaisuuksien lisäämiseen niiden hiomisen sijaan, joten sovellus voi vaikuttaa
tästä syystä melko paljaalta esimerkiksi kurssien tai professorien sivuja luettaessa. Huom että kursseilla oleva ns. opitosuunnitelma
kurssin suorittamiseen ei taida toimia vielä halutusti, koska jätin sen kehittämisen kesken tultuani siihen tulokseen, että courselist
hoitaa melko lailla saman asian. Käytin siihen kuitenkin sen verran vaivaa, että halusin jättää työn jäljet näkyville ja ehkä 
idean saa irti. Voi myös olla että sen viimeisin versio toimii halutusti, mutta en ole tarkistanut.

Opiskelijat voivat sovelluksessa selata kursseja ja niiden opettajia, tai opettajia ja heidän kurssejaan. Kursseista näkyy
esitietovaatimukset, joita pääsee tutkimaan klikkaamalla. Oppilaat voivat myös tehdä kurssisuunnitelman, joka on käytännössä 
lista kursseja joihin voi lisätä uuden vain, jos sen esitietona olevat kurssit on jo lisätty. Tämän on vähän oudon tuntuinen funktio,
koska kursseilla ei ole alkamis- ja loppumispäivämääriä, joten kunnollista opintosuunnitelmaa ei oikein voi tehdä. 

Opettajat voivat myös selata kursseja sekä lisätä ja poistaa niitä. Lisätessään kursseja he voivat valita haluamansa esitietovaatimukset,
ja kurssin poistaminen poistaa sen muiden kurssien esitietovaatimuksista. Opettajien My courses- sivu on erilainen kuin oppilaiden, sillä
se listaa opettajan järjestämät kurssit eikä anna mahdollisuutta tehdä suunnitelmaa. Sovellukseen sisältyy rekisteröinti
ja kirjautuminen, joiden yhteydessä käyttäjän antama syöte tarkistetaan sql-injektion varalta. Opettajien syötettä kurssia
luodessa ei tarkisteta, koska heihin luotetaan (ja tekijä jäisi kiinni helposti).

Olen käyttänyt aika paljon aikaa ja vaivaa sovellukseen ja olen tyytyväinen siitä, mitä olen saanut aikaan (paitsi ulkoasu
on aika kammottava, ja menee sitä hirveämmäksi mitä enemmän yritän sitä korjailla). Sovelluksessa on kuitenkin selviä puutteita,
jotka myönnän itsekin. Kysymys on siis; kuinka paljon enempää kurssin läpipääsemiseen (kunnialla) vaaditaan. 

Tähän listaan asioita, joita voisin lisätä:
-Kursseille päivämäärät ja/tai jotain muuta niiden omille sivuilleen
-Ulkoasun yleinen parantelu (etenkin /mycourses-sivu)
-Opettajien sivuille jotain uutta, vaikka About Me-osio
-Kunnollinen course plan johon voi aikatauluttaa kursseja (vaatisi jo jonkin verran työtä)
-app-tiedoston wall of textin jaotteleminen pienempiin osiin (tämä pitäisi olla jo, pahoittelut)

Muutkin ehdotukset ovat tervetulleita.