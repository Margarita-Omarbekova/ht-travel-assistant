import os
from typing import Any, Dict, List

import httpx
from fastapi import FastAPI, Header, HTTPException, Request

app = FastAPI(title="HT Travel Assistant")

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

SYSTEM_PROMPT = """
Ты — HT Travel Assistant, тревел-ассистент HT.KZ.

Твоя задача — сначала понять, какой отдых нужен пользователю, и только потом
переходить к конкретным продуктам.

Принципы:
1. Не начинай с продажи тура.
2. Выясняй потребности естественным диалогом, без анкеты из множества вопросов.
3. Учитывай состав туристов, возраст детей, даты и сезон, бюджет, город вылета,
   длительность, предпочтения и ограничения.
4. Рекомендуй не просто страну, а при необходимости регион, курорт, район,
   сезонный сценарий и подходящий досуг.
5. Объясняй, почему рекомендация подходит именно этому пользователю.
6. Учитывай сезонность внутри страны: разные побережья, бухты, районы и курорты
   могут быть лучше в разные месяцы.
7. После выбора сценария поездки помогай понять, как ее лучше собрать:
   пакетный тур или отдельно перелет + отель, питание, трансфер, страховка,
   экскурсии и другие услуги.
8. При сравнении вариантов допускай диапазон от бюджетного до премиального.
9. Не выдумывай актуальные цены, наличие, визовые правила и другие данные,
   которые требуют свежей проверки. Если таких данных нет, прямо скажи это.
10. Отвечай по-русски, если пользователь не перешел на другой язык.
11. Задавай за раз максимум один действительно важный уточняющий вопрос.
"""

conversation_memory: Dict[int, List[Dict[str, str]]] = {}


async def telegram_send_message(chat_id: int, text: str) -> None:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": text},
        )
        response.raise_for_status()


def extract_openai_text(data: Dict[str, Any]) -> str:
    for item in data.get("output", []):
        for part in item.get("content", []):
            if part.get("type") == "output_text" and part.get("text"):
                return part["text"].strip()
    return "Не получилось сформировать ответ. Попробуй написать ещё раз."


async def ask_openai(chat_id: int, user_text: str) -> str:
    history = conversation_memory.setdefault(chat_id, [])
    history.append({"role": "user", "content": user_text})
    history[:] = history[-12:]

    transcript = "\n".join(
        f"{'Пользователь' if m['role'] == 'user' else 'Ассистент'}: {m['content']}"
        for m in history
    )

    payload = {
        "model": OPENAI_MODEL,
        "instructions": SYSTEM_PROMPT,
        "input": transcript,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        response.raise_for_status()
        answer = extract_openai_text(response.json())

    history.append({"role": "assistant", "content": answer})
    history[:] = history[-12:]
    return answer


@app.get("/")
async def root():
    return {"status": "ok", "service": "ht-travel-assistant"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    if WEBHOOK_SECRET and x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
        raise HTTPException(status_code=403, detail="Invalid webhook secret")

    update = await request.json()
    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")
    text = (message.get("text") or "").strip()

    if not chat_id or not text:
        return {"ok": True}

    if text.startswith("/start"):
        conversation_memory.pop(chat_id, None)
        reply = (
            "Давай спланируем новое путешествие.\n\n"
            "Расскажи, какого отдыха тебе сейчас хочется. Можно вообще без страны: "
            "море и отдых, впечатления и прогулки, природа, поездка с детьми, "
            "романтическое путешествие — или что-то совсем другое."
        )
    elif text.startswith("/favorites"):
        reply = (
            "Сохранённые путешествия появятся здесь после подключения базы данных. "
            "Сейчас мы тестируем основной сценарий подбора."
        )
    elif text.startswith("/history"):
        reply = "Завершённые путешествия появятся здесь после подключения истории поездок."
    elif text.startswith("/manager"):
        reply = (
            "Передача диалога менеджеру будет следующим этапом. "
            "Позже здесь сможем передавать менеджеру краткое резюме твоего запроса."
        )
    else:
        try:
            reply = await ask_openai(chat_id, text)
        except httpx.HTTPStatusError as e:
            print("OpenAI HTTP error:", e.response.status_code, e.response.text)
            reply = "Сейчас не получилось обратиться к ассистенту. Попробуй ещё раз чуть позже."
        except Exception as e:
            print("Unexpected error:", repr(e))
            reply = "Произошла техническая ошибка. Попробуй ещё раз."

    await telegram_send_message(chat_id, reply)
    return {"ok": True}
