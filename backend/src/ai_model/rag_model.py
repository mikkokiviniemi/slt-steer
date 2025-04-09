from google import genai
from google.genai import types

class RagModel:
    def __init__(self, api_key, temperature=0.5, max_output_tokens=500, model="gemini-2.0-flash-lite"):

        self.client = genai.Client(api_key=api_key)
        self.system_instruction = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context and chat history to answer the question. "
            "Do not use any outside knowledge or make assumptions. "
            "Use three sentences maximum for the main answer and keep the response concise. "

            "If the question is in English and the information is found in the context, first provide a concise answer. "
            "Then, naturally continue the conversation by asking a relevant follow-up question based on the user's query and chat history. "

            "If the question is in Finnish and the information is found in the context, first provide a concise answer. "
            "Sen jälkeen jatka keskustelua luontevasti kysymällä aiheeseen liittyvän jatkokysymyksen, joka auttaa käyttäjää syventämään ymmärrystään ottaen huomioon aikaisemman keskustelun. "

            "If the question is in English and the information is not found in the context, say: "
            "'Unfortunately, I do not have enough information on the topic you asked about. I recommend reaching out to a specialist or your healthcare provider if needed.' "
            "Then, naturally ask a relevant follow-up question based on the chat history to better understand the user's concern. "

            "If the question is in Finnish and the information is not found in the context, say: "
            "'Valitettavasti minulla ei ole riittävästi tietoa esittämääsi aiheeseen. Suosittelen ottamaan yhteyttä asiantuntijaan tai hoitavaan tahoon tarvittaessa.' "
            "Tämän jälkeen kysy luontevasti jatkokysymys, joka auttaa käyttäjää tarkentamaan tilannettaan ottaen huomioon aikaisemman keskustelun. "
        )

        self.chat = self.client.chats.create(
                        model=model,
                        config=types.GenerateContentConfig(
                            system_instruction=self.system_instruction,
                            temperature = temperature,
                            max_output_tokens = max_output_tokens
                        ),
                    )

    def generate_response(self, user_input: str) -> str:
        response = self.chat.send_message(user_input)
        return response.text
    