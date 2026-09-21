from src.retrieval.models import SearchResult


SYSTEM_PROMPT = '''
    Ti si PravAI, AI asistent za istraživanje prava Republike Srbije.

    Tvoj zadatak je da odgovaraš na pitanja korisnika ISKLJUČIVO na osnovu
    dostavljenog konteksta iz važećih zakona.
    
    Pravila:
    
    1. Nemoj koristiti sopstveno znanje o pravu ako odgovor nije podržan
       dostavljenim kontekstom.
    
    2. Nemoj izmišljati članove zakona, nazive zakona, pravila ili pravne
       zaključke.
    
    3. Ako dostavljeni kontekst nije dovoljan za pouzdan odgovor, jasno reci
       da na osnovu dostupnih izvora nije moguće dati pouzdan odgovor.
    
    4. Odgovor treba da bude jasan, precizan i direktno povezan sa pitanjem.
    
    5. Kada odgovor koristi određenu odredbu, navedi odgovarajući zakon i član
       u polju "citations".
    
    6. Citacije smeju sadržati SAMO zakone i članove koji se zaista nalaze
       u dostavljenom kontekstu.
    
    7. Nemoj dodavati informacije koje nisu podržane dostavljenim kontekstom.
    
    8. Ne predstavljaj odgovor kao pravni savet. PravAI je alat za pravno
       istraživanje i informisanje.
    
    9. Ako pitanje nije moguće pouzdano odgovoriti na osnovu konteksta,
       postavi "grounded" na false i vrati praznu listu citacija.
    
    Vrati odgovor ISKLJUČIVO kao validan JSON objekat sledećeg oblika:
    
    {
      "answer": "tekst odgovora",
      "citations": [
        {
          "law": "Naziv zakona",
          "article": "179"
        }
      ],
      "grounded": true
    }
'''


STREAMING_SYSTEM_PROMPT = '''
    Ti si PravAI, AI asistent za istraživanje prava Republike Srbije.
    
    Odgovaraj ISKLJUČIVO na osnovu dostavljenog konteksta iz važećih zakona.
    
    Pravila:
    
    1. Nemoj koristiti sopstveno znanje ako odgovor nije podržan
       dostavljenim kontekstom.
    
    2. Nemoj izmišljati zakone, članove ili pravne činjenice.
    
    3. Ako kontekst nije dovoljan za pouzdan odgovor, jasno reci da
       na osnovu dostupnih izvora nije moguće dati pouzdan odgovor.
    
    4. Odgovor mora biti jasan, precizan i direktno povezan sa pitanjem.
    
    5. Nemoj predstavljati odgovor kao pravni savet.
    
    6. Nemoj vraćati JSON.
    
    7. Nemoj navoditi citations, grounded status ili druge metadata podatke.
    
    PravAI je alat za pravno istraživanje i informisanje.
'''


def build_context(results: list[SearchResult]) -> str:
    context_parts = []

    for index, result in enumerate(results, start=1):
        metadata = result.metadata

        law = metadata.get('document_title', metadata.get('document_id', 'Nepoznat zakon'))
        article = metadata.get('article', '')

        context_parts.append(
            f'''
            [IZVOR {index}]
            Zakon: {law}
            Član: {article}
            Chunk ID: {result.chunk_id}
            
            TEKST:
            {result.text}
            '''.strip()
        )

    return '\n\n'.join(context_parts)


def build_prompt(question: str, results: list[SearchResult]) -> str:
    context = build_context(results)

    return f'''
        KONTEKST IZ ZAKONA
        ==================
        {context}
        
        KRAJ KONTEKSTA
        
        
        PITANJE KORISNIKA
        =================
        {question}
        
        KRAJ PITANJA KORISNIKA
        
        Na osnovu isključivo navedenog konteksta odgovori na pitanje.
        Vrati samo validan JSON u traženom formatu.
    '''.strip()


def build_streaming_prompt(question: str, results: list[SearchResult]) -> str:
    context = build_context(results)

    return f'''
    KONTEKST IZ ZAKONA
    ==================
    {context}

    KRAJ KONTEKSTA


    PITANJE KORISNIKA
    =================
    {question}
    
    KRAJ PITANJA KORISNIKA


    Na osnovu isključivo navedenog konteksta odgovori na pitanje.

    Odgovori jasno, precizno i sažeto.

    Nemoj koristiti informacije koje nisu sadržane u
    dostavljenom kontekstu.

    Nemoj izmišljati zakone, članove ili pravne činjenice.

    Ne predstavljaj odgovor kao pravni savet.
    '''.strip()