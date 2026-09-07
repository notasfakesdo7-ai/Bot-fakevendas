import logging
import requests
import base64
import io
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Ativa o sistema de logs
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

TELEGRAM_TOKEN = "8820841901:AAE7EBhoiuHAFpT11V2DwGTEr7Owlkn5Mg0"

# Credenciais e Base URL da pro PAYbr extraídas das imagens
PROPIX_CLIENT_ID = "live_9f1f14cc157574e085a4d3cc40b4d479"
PROPIX_SECRET = "sk_413fbb57236ff43c1f2d90f6c524101492c913d163e8c3115aca5cf9beb1f1a0"
PROPIX_BASE_URL = "https://api.propixbr.com"

# Função auxiliar para gerar o Pix na pro PAYbr (Cash-In)
def gerar_pix_propix(valor: float, descricao: str):
    url = f"{PROPIX_BASE_URL}/api/v1/deposit"
    headers = {
        "x-client-id": PROPIX_CLIENT_ID,
        "x-client-secret": PROPIX_SECRET,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "amount": round(float(valor), 2),
        "description": str(descricao),
        "payerName": "Cliente Telegram",
        "payerDocument": "12345678909"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        print(f"Status Code da pro PAYbr: {response.status_code}")
        print(f"Resposta da pro PAYbr: {response.text}")
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return None

# /start - Mensagem de boas-vindas com a foto local e o botão "Comprar pacote aqui"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [[InlineKeyboardButton("Comprar pacote aqui", callback_data="menu_anos")]]
    reply_markup = InlineKeyboardMarkup(teclado)
    
    texto = (
        "Aproveite de conteúdos exclusivos e atualizados. Só encontra aqui🔥\n\n"
        "• Os cp mais gostosos da internet\n"
        "• Vídeos fazendo o ato com elas dormindo\n"
        "• 2 ou mais em cima delas\n"
        "• Pegando a força\n"
        "• BQT e Anal\n"
        "• Masculino e Feminino\n"
        "• Varios videos BR\n"
        "• Videos com todos fetiches possíveis\n\n"
        "⚠️ Bom proveito e cuidado onde vai guardar os conteúdos🤫\n\n"
        "Caso ocorra algum erro no pagamento entre em contato com o Suporte: @suportecp69"
    )
    
    try:
        with open("lisa bb.jpeg", "rb") as foto_arquivo:
            await update.message.reply_photo(
                photo=foto_arquivo,
                caption=texto,
                reply_markup=reply_markup,
                parse_mode="Markdown"
            )
    except Exception:
        await update.message.reply_text(
            text=texto,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

# Callback para gerenciar todos os cliques nos botões do fluxo
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # 1. Clicou em "Comprar pacote aqui" -> Escolha do Ano
    if data == "menu_anos":
        texto_anos = (
            "Escolha os vídeos a partir de qual ano:\n\n"
            "• 2002 a 2015 a partir de R$ 18,99\n"
            "• 2016 a 2026 a partir de R$ 21,60"
        )
        teclado = [
            [InlineKeyboardButton("Vídeos de 2002 a 2015", callback_data="ano_2002_2015")],
            [InlineKeyboardButton("Vídeos de 2016 a 2026", callback_data="ano_2016_2026")]
        ]
        await query.message.reply_text(text=texto_anos, reply_markup=InlineKeyboardMarkup(teclado))

    # 2. Salvou o Ano escolhido -> Vai para a escolha do Pacote com os preços corretos do ano
    elif data.startswith("ano_"):
        context.user_data["ano"] = data 
        
        if data == "ano_2002_2015":
            p_basico, p_vip, p_prem = 18.99, 22.99, 26.99
        else:
            p_basico, p_vip, p_prem = 21.60, 25.60, 29.60

        texto_pacotes = (
            "Escolha seu pacote:\n\n"
            "⭐ **Básico:** Vai 500 vídeos + Link do Mega com 1k de vídeos.\n\n"
            "🌟 **VIP:** Vai 1.000 vídeos + Link do Mega com 1.8k de vídeos.\n\n"
            "👑 **Premium:** 1.900 Vídeos + Link do Mega com 3k de vídeos."
        )
        teclado = [
            [InlineKeyboardButton(f"⭐️ Básico: a partir de R$ {p_basico:.2f}", callback_data="pacote_basico")],
            [InlineKeyboardButton(f"🌟 VIP: a partir de R$ {p_vip:.2f}", callback_data="pacote_vip")],
            [InlineKeyboardButton(f"👑 Premium: a partir de R$ {p_prem:.2f}", callback_data="pacote_premium")]
        ]
        await query.message.reply_text(text=texto_pacotes, reply_markup=InlineKeyboardMarkup(teclado), parse_mode="Markdown")

    # 3. Salvou o Pacote escolhido -> Vai para a escolha da Categoria (Idade) com acréscimos (+4 e +8)
    elif data.startswith("pacote_"):
        context.user_data["pacote"] = data 
        
        ano_escolhido = context.user_data.get("ano", "ano_2002_2015")
        
        if ano_escolhido == "ano_2002_2015":
            if data == "pacote_basico": base = 18.99
            elif data == "pacote_vip": base = 22.99
            else: base = 26.99
        else: 
            if data == "pacote_basico": base = 21.60
            elif data == "pacote_vip": base = 25.60
            else: base = 29.60
            
        p1 = base
        p2 = base + 4.00
        p3 = base + 8.00
        
        texto_categorias = (
            "Escolha a categoria:\n\n"
            f"1️⃣ Idade 12 a 15 anos — R$ {p1:.2f}\n"
            f"2️⃣ Idade de 7 a 11 anos — R$ {p2:.2f}\n"
            f"3️⃣ Idade de 1 a 6 anos — R$ {p3:.2f}"
        )
        teclado = [
            [InlineKeyboardButton(f"1️⃣ 12 a 15 anos (R$ {p1:.2f})", callback_data="cat_1")],
            [InlineKeyboardButton(f"2️⃣ 7 a 11 anos (R$ {p2:.2f})", callback_data="cat_2")],
            [InlineKeyboardButton(f"3️⃣ 1 a 6 anos (R$ {p3:.2f})", callback_data="cat_3")]
        ]
        await query.message.reply_text(text=texto_categorias, reply_markup=InlineKeyboardMarkup(teclado))

    # 4. Finalizou a escolha da Categoria -> Gera o Pix real via pro PAYbr e mostra o resumo + QR Code (Base64)
    elif data.startswith("cat_"):
        ano_escolhido = context.user_data.get("ano", "ano_2002_2015")
        pacote = context.user_data.get("pacote", "pacote_basico")
        
        if ano_escolhido == "ano_2002_2015":
            if pacote == "pacote_basico": base = 18.99
            elif pacote == "pacote_vip": base = 22.99
            else: base = 26.99
        else:
            if pacote == "pacote_basico": base = 21.60
            elif pacote == "pacote_vip": base = 25.60
            else: base = 29.60
            
        if data == "cat_1":
            preco_final = base
            cat_nome = "Idade 12 a 15 anos"
        elif data == "cat_2":
            preco_final = base + 4.00
            cat_nome = "Idade de 7 a 11 anos"
        else:
            preco_final = base + 8.00
            cat_nome = "Idade de 1 a 6 anos"

        # Mensagem de carregamento
        loading_msg = await query.message.reply_text("Gerando sua cobrança Pix, aguarde um instante...")

        # Chamada real para criar o Pix na pro PAYbr
        resposta_pix = gerar_pix_propix(preco_final, f"Compra Pacote - {cat_nome}")

        # Deleta a mensagem de carregamento
        await loading_msg.delete()

        if resposta_pix:
            copia_e_cola = resposta_pix.get("copyPaste") or "Chave Pix indisponível"
            qrcode_base64 = resposta_pix.get("qrcodeUrl")
            
            resumo = (
                "✅ **Pedido Confirmado!**\n\n"
                f"• **Categoria:** {cat_nome}\n"
                f"• **Valor Total:** R$ {preco_final:.2f}\n\n"
                "Utilize o Pix Copia e Cola abaixo:\n\n"
                f"`{copia_e_cola}`\n\n"
                "Após o pagamento, envie o comprovante para o suporte: @suportecp69"
            )

            # Converte e envia o QR Code em Base64 como foto
            if qrcode_base64 and "base64," in qrcode_base64:
                try:
                    base64_data = qrcode_base64.split("base64,")[1]
                    image_bytes = base64.b64decode(base64_data)
                    photo_file = io.BytesIO(image_bytes)
                    photo_file.name = "qrcode.png"

                    await query.message.reply_photo(
                        photo=photo_file,
                        caption=resumo,
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"Erro ao converter QR Code: {e}")
                    await query.message.reply_text(text=resumo, parse_mode="Markdown")
            else:
                await query.message.reply_text(text=resumo, parse_mode="Markdown")
        else:
            resumo = (
                "⚠️ Ocorreu um erro ao gerar o Pix automático com o gateway.\n\n"
                f"• **Categoria:** {cat_nome}\n"
                f"• **Valor Total:** R$ {preco_final:.2f}\n\n"
                "Entre em contato direto com o suporte para concluir: @suportecp69"
            )
            await query.message.reply_text(text=resumo, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot rodando com sucesso! Pressione Ctrl+C para parar.")
    app.run_polling()

if __name__ == "__main__":
    main()