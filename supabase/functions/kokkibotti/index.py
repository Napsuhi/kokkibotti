#API-avain lisätty holviin
# Versio 2
import os
from openai import OpenAI

# Oikea, turvallinen tapa
import os
API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

# Tämä funktio on välttämätön, jotta selain voi keskustella tämän funktion kanssa.
# Se hoitaa ns. CORS-otsikot. Kopioi tämä sellaisenaan.
def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    }

async def handler(request):
    # Tämä on erikoistoiminto, joka vastaa selaimen "esikyselyyn". Kopioi sellaisenaan.
    if request.method == 'OPTIONS':
        return {'body': 'ok', 'headers': cors_headers(), 'status': 200}

    # Vastaanotetaan data, jonka selain lähetti (ei enää input-komentoa!)
    data = await request.json()
    ainekset = data.get('ainekset')

    if not ainekset:
        return {'body': {'error': 'Aineksia ei annettu.'}, 'headers': cors_headers(), 'status': 400}

    # TÄMÄ OSA ON TÄYSIN SAMA KUIN VANHASSA KOODISSASI!
    # Ainoa muutos on, että system-viesti on nyt tässä.
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Olet Cittarin kokkibotti, ystävällinen ja avulias ruoka-asiantuntija. Tehtäväsi on luoda helppo resepti, joka käyttää PÄÄASIALLISESTI käyttäjän antamia aineksia. ÄLÄ KOSKAAN EHDOTA AINEKSIA, JOITA KÄYTTÄJÄ EI OLE ANTANUT. Jos käyttäjän antamista aineksista ei voi mitenkään valmistaa järkevää ateriaa, sinun tulee kohteliaasti todeta se. Ehdota sen jälkeen reseptiä, joka käyttää vain yhtä tai kahta sopivinta niistä aineksista, jotka käyttäjä alun perin antoi. Suosi aina proteiininlähdettä (kuten lihaa, kanaa tai kalaa) reseptin pääraaka-aineena."},
            {"role": "user", "content": f"Minulla on seuraavat ainekset: {ainekset}. Anna helppo arkiruokaresepti."}
        ]
    )
    vastaus = completion.choices[0].message.content

    # Palautetaan vastaus selaimelle (ei enää print-komentoa!)
    return {'body': {'resepti': vastaus}, 'headers': cors_headers(), 'status': 200}

# Tämä on Supabasen vaatima komento funktion käynnistämiseen.
# Se käyttää Deno-nimistä taustateknologiaa Python-koodin ajamiseen.
Deno.serve(handler)