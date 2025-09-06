document.addEventListener('DOMContentLoaded', () => {
    // --- TÄRKEÄÄ: LIITÄ OMA FUNKTION URL TÄHÄN ---
    const KOKKIBOTTI_URL = "https://pxfzfabavwembuauwsuo.supabase.co/functions/v1/kokkibotti";

    const reseptiNappi = document.querySelector('button');
    const ainesInput = document.querySelector('#aineksetInput');
    const vastausAlue = document.querySelector('#vastausAlue');

    reseptiNappi.addEventListener('click', async () => {
        const ainekset = ainesInput.value;
        if (!ainekset) {
            alert('Kirjoita ensin ainekset!');
            return;
        }

        vastausAlue.innerHTML = `<p>Cittarin kokkibotti miettii hetken...</p>`;
        reseptiNappi.disabled = true; // Estetään tuplaklikkaus

        try {
            // Lähetetään verkkopyyntö sinun pilvifunktiollesi!
            const response = await fetch(KOKKIBOTTI_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ainekset: ainekset })
            });

            if (!response.ok) {
                throw new Error(`Verkkovirhe: ${response.statusText}`);
            }

            const data = await response.json();
            // Näytetään botin vastaus sivulla ja korvataan rivinvaihdot HTML-tageilla
            vastausAlue.innerHTML = `<p>${data.resepti.replace(/\n/g, '<br>')}</p>`;

        } catch (error) {
            console.error('Tapahtui virhe:', error);
            vastausAlue.innerHTML = `<p>Pahoittelut, jokin meni pieleen. Yritä hetken päästä uudelleen.</p>`;
        } finally {
            reseptiNappi.disabled = false; // Sallitaan napin käyttö taas
        }
    });
});