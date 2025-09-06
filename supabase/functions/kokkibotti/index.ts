// Pakotetaan uusi julkaisu API-avaimen lisäämisen jälkeen
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts'
import OpenAI from 'npm:openai'

// Alustetaan OpenAI-asiakas. Se hakee avaimen automaattisesti Supabasen Secret-holvista.
const client = new OpenAI({
  apiKey: Deno.env.get('OPENAI_API_KEY'),
})

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { ainekset } = await req.json()
    if (!ainekset) {
      throw new Error('Aineksia ei annettu.')
    }

    const completion = await client.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {
          role: 'system',
          content: "Olet Cittarin kokkibotti, ystävällinen ja avulias ruoka-asiantuntija. Tehtäväsi on luoda helppo resepti, joka käyttää PÄÄASIALLISESTI käyttäjän antamia aineksia. ÄLÄ KOSKAAN EHDOTA AINEKSIA, JOITA KÄYTTÄJÄ EI OLE ANTANUT. Jos käyttäjän antamista aineksista ei voi mitenkään valmistaa järkevää ateriaa, sinun tulee kohteliaasti todeta se. Ehdota sen jälkeen reseptiä, joka käyttää vain yhtä tai kahta sopivinta niistä aineksista, jotka käyttäjä alun perin antoi. Suosi aina proteiininlähdettä (kuten lihaa, kanaa tai kalaa) reseptin pääraaka-aineena."
        },
        {
          role: 'user',
          content: `Minulla on seuraavat ainekset: ${ainekset}. Anna helppo arkiruokaresepti.`,
        },
      ],
    })

    const vastaus = completion.choices[0].message.content
    return new Response(JSON.stringify({ resepti: vastaus }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    })
  } catch (error) {
    console.error(error)
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500,
    })
  }
})