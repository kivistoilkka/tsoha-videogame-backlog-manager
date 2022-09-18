# Videogame Backlog Manager
Sovelluksen avulla käyttäjä voi ylläpitää tietokantaa omistamistaan ja pelaamistaan videopeleistä. Käyttäjä voi lisätä pelejä kokoelmaansa ja tallentaa peliin liittyviä tietoja, kuten onko käyttäjä ehtinyt pelaamaan peliä, onko pelin tarina läpäisty, onko peli suoritettu kokonaisuudessaan ja minkä numeroarvion käyttäjä haluaa antaa pelille. Sovellus myös näyttää etusivulla yhteenvedon suosituimmista peleistä, niiden läpäisyprosenteista ja pelin arvioiden keskiarvon. Linkkien kautta pääsee tarkastelemaan kaikkien pelien listaa ja tarkemmin kunkin pelin tietoja. Jokainen kirjautunut käyttäjä on peruskäyttäjä tai ylläpitäjä.

Sovelluksen ominaisuuksia ovat:
- Kaikki vierailijat voivat tarkastella suosituimpien pelien listaa ja linkkien kautta peleihin liittyviä yhteenvetoja ja arvioita.
- Käyttäjä voi luoda itselleen tunnuksen ja kirjautua sisään ja ulos.
- Käyttäjä voi lisätä sovelluksen tietokannassa olevan pelin omaan kokoelmaansa.
- Käyttäjä voi päivittää omassa kokoelmassaan olevan pelin tietoja.
  - Onko pelin pelaaminen aloitettu.
  - Onko pelin tarina läpäisty.
  - Onko peli pelattu läpi 100%.
- Käyttäjä voi poistaa pelin kokoelmastaan
  - Peli piilotetaan, pelin uudelleen lisääminen tuo pelin uudestaan näkyviin
- Käyttäjä voi kirjoittaa pelistä arvion.
  - Arvio pelistä asteikolla 0-10.
  - Sanallinen arvio pelistä.
  - Arvion näkyvyys muille käyttäjille.
- Ylläpitäjä voi lisätä pelejä sovelluksen tietokantaan.
  - Pelin nimi
  - Pelin alusta (esim. pc, pelikonsoli)
- Ylläpitäjä voi piilottaa pelejä tietokannasta.
- Ylläpitäjä voi lisätä pelialustoja tietokantaan.
- Ylläpitäjä voi piilottaa pelialustoja tietokannasta.

## Tietokannan rakenne
```mermaid
classDiagram
  class users {
    id INTEGER
    username TEXT
    password TEXT
    is_admin BOOLEAN
  }
  class games {
    id INTEGER
    name TEXT
    platform_id INTEGER
    visible BOOLEAN
  }
  class platforms {
    id INTEGER
    name TEXT
    visible BOOLEAN
  }
  class collection_items {
    id INTEGER
    user_id INTEGER
    game_id INTEGER
    story_completed BOOLEAN
    full_completion BOOLEAN
    visible BOOLEAN
  }
  class game_reviews {
    id INTEGER
    user_id INTEGER
    game_id INTEGER
    rating INTEGER
    comments TEXT
    review_added TIMESTAMP
    visible BOOLEAN
  }

  users "1" -- "*" collection_items
  games "1" -- "*" collection_items
  users "1" -- "*" game_reviews
  games "1" -- "*" game_reviews
  games "*" --  "1" platforms
```