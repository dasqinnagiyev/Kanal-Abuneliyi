import time
import logging
from config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="😇 Bu 'kanala' gir sonra 'Səsimi aç' düyməsinə toxun.", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="❗ Adminlər tərəfindən başqa bir səbəbə görə səssizə alınmısan.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention}on} səsini açmağa çalışır, lakin mən onun səsini aça bilmirəm, çünki bu çatda admin deyiləm, məni yenidən admin kimi əlavə et.**\n__#Burdan çıxıram...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❗ Xəbərdarlıq: Əgər sərbəst danışa bilirsənsə, düyməni basma.", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      if channel.startswith("-"):
          url = client.export_chat_invite_link(int(channel))
      else:
          url = f"https://t.me/{channel}"
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              f"Hi {message.from_user.mention}, Sən, mənim [Kanalıma]({url}) **Abunə deyilsən**. Zəhmət olmasa 👉 [Qatıl]({url}) Və səssizdən çıxmaq üçün **Aşağıdaki düyməyə toxun** 👇...",
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
             [
                 [
                     InlineKeyboardButton("🌙 Abunə ol", url=url)
                 ],
                 [
                     InlineKeyboardButton("🔕 Səsimi Aç", callback_data="onUnMuteRequest")
                 ]
             ]
         )
           )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **Mən burada admin deyiləm.**\n__Məni admin et və grupa yenidən əlavə et.\n#Burdan çıxıram...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **Mən bu [kanalda]({url}) admin deyiləm**\n__Məni kanalda admin et və yenidən əlavə et.\n#Burdan çıxıram...__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub", "abuneol", "qosul"]) & ~filters.private)
def fsub(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable", "yox", "dayan", "bagla"):
        sql.disapprove(chat_id)
        message.reply_text("❎ **Kanal Abunəliyi Uğurla Deaktiv edildi.**")
      elif input_str.lower() in ('clear', 'sil'):
        sent_message = message.reply_text('**Səsini bağladıqlarımın hamısının səsini açıram...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **Səsini bağladıqlarımın hamısının səsini açdım.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **Mən bu grupda admin deyiləm.**\n__Mən üzvlərin səsini aça bilmirəm, çünki bu grupda admin deyiləm, məni admin et.__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          if input_str.startswith("-"):
              url = client.export_chat_invite_link(int(input_str))
          else:
              url = f"https://t.me/{input_str}"
          message.reply_text(f"☑️ **Kanal abunəliyi aktiv edildi**\n__Bütün grup istifadəçiləri grupa mesaj yaza bilmək üçün bu [kanala]({url}) abunə olmalıdır..__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **Bu Kanalda Admin Deyiləm**\n__mən bi [kanalda]({url}) admin deyiləm. Kanal abunəliyini aktivləşdirmək üçün məni admin kimi əlavə et.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Kanal İstifadəçi Adı/ID Yanlışdır.**")
        except Exception as err:
          message.reply_text(f"❗ **XƏTA:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        my_channel = sql.fs_settings(chat_id).channel
        if my_channel.startswith("-"):
            url = client.export_chat_invite_link(int(input_str))
        else:
            url = f"https://t.me/{my_channel}"
        message.reply_text(f"☑️ **Bu grupda kanal abunəliyi aktiv edilib.**\n__Kanal abunəliyi bu [Kanal]({url}) üçün aktivdir.__", disable_web_page_preview=True)
      else:
        message.reply_text("❎ **Bu grupda Kanal Abunəliyi deaktiv edilib.**")
  else:
      message.reply_text("❗ **Qrup Yaradıcısı Tələb Edilir**\n__Bunun üçün siz qrup yaradıcısı olmalısınız.__")
