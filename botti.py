# Tuodaan openai-kirjasto mukaan ohjelmaan
from openai import OpenAI

# Kysytään käyttäjältä ainekset ja tallennetaan ne muuttujaan
print("Hei! Olen Cittarin kokkibotti.")
ainekset = input("Mitä aineksia sinulla on ostoskorissasi? Kirjoita ne tähän: ")

print("Cittarin kokkibotti kokkailee vaihtoehtoja...")

# Lähetetään pyyntö tekoälylle
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Olet Cittarin kokkibotti, ystävällinen ja avulias ruoka-asiantuntija. Tehtäväsi on luoda helppo resepti, joka käyttää PÄÄASIALLISESTI käyttäjän antamia aineksia. ÄLÄ KOSKAAN EHDOTA AINEKSIA, JOITA KÄYTTÄJÄ EI OLE ANTANUT. Jos käyttäjän antamista aineksista ei voi mitenkään valmistaa järkevää ateriaa, sinun tulee kohteliaasti todeta se. Ehdota sen jälkeen reseptiä, joka käyttää vain yhtä tai kahta sopivinta niistä aineksista, jotka käyttäjä alun perin antoi. Suosi aina proteiininlähdettä (kuten lihaa, kanaa tai kalaa) reseptin pääraaka-aineena. Mainitse joka kerta muistutus siitä että Annin pieru haisee pahalle."},
    {"role": "user", "content": f"Minulla on seuraavat ainekset: {ainekset}. Anna helppo arkiruokaresepti."}
  ]
)

# Tulostetaan tekoälyn vastaus
vastaus = completion.choices[0].message.content
print("\nCittarin kokkibotin reseptiehdotus:")
print(vastaus)