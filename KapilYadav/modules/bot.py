import asyncio
import logging
import sys
import json
from datetime import datetime
from os import execl

from telethon import events, Button
from telethon.events import ChatAction
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest
from telethon.tl.types import ChatBannedRights, ChatAdminRights

from config import X1, X2, X3, X4, X5, X6, X7, X8, X9, X10, SUDO_USERS, CMD_HNDLR as hl

logging.basicConfig(level=logging.INFO)

clients = [X1, X2, X3, X4, X5, X6, X7, X8, X9, X10]

CONFIG_FILE = "config_store.json"
try:
    with open(CONFIG_FILE) as f:
        STORED_CONFIG = json.load(f)
except:
    STORED_CONFIG = {}

async def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(STORED_CONFIG, f)

SHUTDOWN_MODE = {"active": False}
ALIVE_MESSAGE = "💫 **I'm Alive!** 💫\n\n✨ **Bot Status:** Working Fine\n⚡ **Powered By:** [Revenge King](https://t.me/https://t.me/+ub0nytC5h-FhMzc9)"

async def block_if_shutdown(event):
    return SHUTDOWN_MODE["active"] and event.sender_id not in SUDO_USERS

async def ping_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        start = datetime.now()
        msg = await event.reply("•[ 🍹𝗖𝘀𝗻 𝗄𝗲𝘃 🍹 ]•")
        end = datetime.now()
        ms = (end - start).microseconds / 1000
        await msg.edit(
            f"[🍹] ʁọʟọɴ ริกเคิ้ง ᴘαɑα ɪʃ нєʁє\n"
            f"[🏓] αвє αв тєʀα куα нσgα\n"
            f"[⚡] кіσκι ₕну∂αі кαяνі нαі\n\n"
            f"➔ {ms} ms"
        )

async def alive_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        await event.reply(ALIVE_MESSAGE)

async def set_alive_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        global ALIVE_MESSAGE
        text = event.raw_text.split(None, 1)
        if len(text) > 1:
            ALIVE_MESSAGE = text[1]
            await event.reply("Alive message updated successfully!")
        else:
            await event.reply("Please provide the new alive message after the command.")

async def reboot_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        await event.reply(
            "ʁєвσγτ ʁσιε\n"
            "[🍷] 2 міιτ ωαιτ ṗℓєαѕє\n"
            "[🪧] ƒіρ ααяєɢα тєʀі μᴀα ₕнσₑιε ʁєᴡєɴɢєкєιɢ βαβу"
        )
        for x in clients:
            try:
                await x.disconnect()
            except:
                pass
        execl(sys.executable, sys.executable, *sys.argv)

async def shutdown_handler(event):
    if event.sender_id in SUDO_USERS:
        SHUTDOWN_MODE["active"] = True
        await event.reply("Bot is now in shutdown mode. Only the owner can interact.")

async def start_handler(event):
    if event.sender_id in SUDO_USERS:
        SHUTDOWN_MODE["active"] = False
        await event.reply("Bot is now active for all sudo commands.")

async def sudo_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        try:
            reply = await event.get_reply_message()
            args = event.pattern_match.group(1)
            
            if reply:
                target = reply.sender_id
            elif args:
                try:
                    if args.isdigit():
                        target = int(args)
                    else:
                        user = await event.client.get_entity(args)
                        target = user.id
                except ValueError:
                    return await event.reply("Invalid user ID.")
                except Exception as e:
                    return await event.reply(f"Error getting user: {str(e)}")
            else:
                return await event.reply("Reply to a user or provide username/ID.")
                
            if target not in SUDO_USERS:
                SUDO_USERS.append(target)
                await event.reply(f"User {target} added to sudo list.")
            else:
                await event.reply("User is already a sudo user.")
        except Exception as e:
            await event.reply(f"Failed to add sudo: {str(e)}")

async def unsudo_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        try:
            reply = await event.get_reply_message()
            args = event.pattern_match.group(1)
            
            if reply:
                target = reply.sender_id
            elif args:
                try:
                    if args.isdigit():
                        target = int(args)
                    else:
                        user = await event.client.get_entity(args)
                        target = user.id
                except ValueError:
                    return await event.reply("Invalid user ID.")
                except Exception as e:
                    return await event.reply(f"Error getting user: {str(e)}")
            else:
                return await event.reply("Reply to a user or provide username/ID.")
                
            if target in SUDO_USERS:
                SUDO_USERS.remove(target)
                await event.reply(f"User {target} removed from sudo list.")
            else:
                await event.reply("User is not a sudo user.")
        except Exception as e:
            await event.reply(f"Failed to remove sudo: {str(e)}")

async def sudolist_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        if not SUDO_USERS:
            return await event.reply("No sudo users configured.")
            
        message = "**🍷 Sudo Users List 🍷**\n\n"
        for user_id in SUDO_USERS:
            try:
                user = await event.client.get_entity(user_id)
                name = f"{user.first_name} {user.last_name or ''}".strip()
                username = f"@{user.username}" if user.username else "No username"
                message += f"• {name} ({username}) - `{user_id}`\n"
            except:
                message += f"• Unknown user - `{user_id}`\n"
                
        await event.reply(message)

async def group_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        try:
            reply = await event.get_reply_message()
            if not reply: return await event.reply("Reply to a user.")
            user = await event.client.get_entity(reply.sender_id)
            cmd = event.pattern_match.group(1).lower()

            if cmd == "promote":
                rights = ChatAdminRights(
                    post_messages=True,
                    add_admins=False,
                    invite_users=True,
                    change_info=False,
                    ban_users=True,
                    delete_messages=True,
                    pin_messages=True
                )
                await event.client(EditAdminRequest(event.chat_id, user.id, rights, "Admin"))
            elif cmd == "fullpromote":
                rights = ChatAdminRights(
                    post_messages=True,
                    add_admins=True,
                    invite_users=True,
                    change_info=True,
                    ban_users=True,
                    delete_messages=True,
                    pin_messages=True,
                    edit_messages=True
                )
                await event.client(EditAdminRequest(event.chat_id, user.id, rights, "Full Admin"))
            elif cmd == "demote":
                await event.client(EditAdminRequest(event.chat_id, user.id, ChatAdminRights(), ""))
            elif cmd == "ban":
                await event.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=True)))
            elif cmd == "unban":
                await event.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=False)))
            elif cmd == "kick":
                await event.client.kick_participant(event.chat_id, user.id)
            elif cmd == "mute":
                await event.client.edit_permissions(event.chat_id, user.id, send_messages=False)
            elif cmd == "unmute":
                await event.client.edit_permissions(event.chat_id, user.id, send_messages=True)

            await event.reply(f"{cmd.capitalize()} executed.")
        except Exception as e:
            await event.reply(f"Error in {cmd}: {str(e)}")

async def lock_unlock_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id not in SUDO_USERS: return
    try:
        cmd = event.pattern_match.group(1).lower()
        target = event.pattern_match.group(2).lower() if len(event.pattern_match.groups()) > 1 else "all"
        
        permissions = {
            "msg": "send_messages",
            "media": "send_media",
            "stickers": "send_stickers",
            "gifs": "send_gifs",
            "games": "send_games",
            "inline": "send_inline",
            "polls": "send_polls",
            "invite": "invite_users",
            "pin": "pin_messages",
            "changeinfo": "change_info"
        }
        
        if target == "all":
            # Special handling for all permissions
            if cmd == "lock":
                await event.client.edit_permissions(
                    event.chat_id,
                    send_messages=False,
                    send_media=False,
                    send_stickers=False,
                    send_gifs=False,
                    send_games=False,
                    send_inline=False,
                    send_polls=False,
                    invite_users=False,
                    pin_messages=False,
                    change_info=False
                )
            else:  # unlock
                await event.client.edit_permissions(
                    event.chat_id,
                    send_messages=True,
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    send_polls=True,
                    invite_users=True,
                    pin_messages=True,
                    change_info=True
                )
        else:
            if target not in permissions:
                return await event.reply("Invalid type. Use: " + ", ".join(permissions.keys()))
            
            if target == "msg":
                await event.client.edit_permissions(
                    event.chat_id,
                    send_messages=(cmd == "unlock")
                )
            else:
                await event.client.edit_permissions(
                    event.chat_id,
                    **{permissions[target]: (cmd == "unlock")}
                )
        
        await event.reply(f"{cmd.capitalize()}ed `{target}`.")
    except Exception as e:
        await event.reply(f"Error in lock/unlock: {str(e)}")

async def logs_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        await event.reply("Sending logs...")
        await event.client.send_file(event.chat_id, "log.txt")

async def set_text_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        cmd = event.pattern_match.group(1)
        text = event.raw_text.split(None, 1)[1] if len(event.raw_text.split(None, 1)) > 1 else None
        if not text:
            return await event.reply("Provide text.")
        STORED_CONFIG[f"{cmd}_{event.chat_id}"] = text
        await save_config()
        await event.reply(f"{cmd} message saved!")

async def rules_handler(event):
    if await block_if_shutdown(event): return
    text = STORED_CONFIG.get(f"setrules_{event.chat_id}", "No rules set.")
    await event.reply(text)

async def welcome_leave_handler(event):
    if SHUTDOWN_MODE["active"]: return
    chat_id = event.chat_id
    if event.user_joined or event.user_added:
        text = STORED_CONFIG.get(f"setwelcome_{chat_id}", None)
        if text: await event.reply(text)
    elif event.user_left or event.user_kicked:
        text = STORED_CONFIG.get(f"setleave_{chat_id}", None)
        if text: await event.reply(text)

async def echo_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        reply = await event.get_reply_message()
        if reply:
            await event.reply(reply.text)

async def rmecho_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        await event.delete()

async def userinfo_handler(event):
    if await block_if_shutdown(event): return
    if event.sender_id in SUDO_USERS:
        reply = await event.get_reply_message()
        if reply:
            user = await event.client.get_entity(reply.sender_id)
        else:
            args = event.raw_text.split(None, 1)
            if len(args) == 2:
                user = await event.client.get_entity(args[1])
            else:
                return await event.reply("Reply to user or provide username/id.")
        await event.reply(
            f"👤 User Info\n"
            f"• Name: {user.first_name} {user.last_name or ''}\n"
            f"• Username: @{user.username or 'N/A'}\n"
            f"• ID: {user.id}\n"
            f"• Bot: {user.bot}\n"
            f"• Verified: {getattr(user, 'verified', 'N/A')}"
        )

# ─── Register All Commands ───────────────────────────────

for client in clients:
    client.add_event_handler(ping_handler, events.NewMessage(pattern=fr"{hl}ping", incoming=True))
    client.add_event_handler(alive_handler, events.NewMessage(pattern=fr"{hl}alive", incoming=True))
    client.add_event_handler(set_alive_handler, events.NewMessage(pattern=fr"{hl}setalive", incoming=True))
    client.add_event_handler(reboot_handler, events.NewMessage(pattern=fr"{hl}reboot", incoming=True))
    client.add_event_handler(sudo_handler, events.NewMessage(pattern=fr"{hl}sudo(?:\s+(.+))?", incoming=True))
    client.add_event_handler(unsudo_handler, events.NewMessage(pattern=fr"{hl}unsudo(?:\s+(.+))?", incoming=True))
    client.add_event_handler(sudolist_handler, events.NewMessage(pattern=fr"{hl}sudolist", incoming=True))
    client.add_event_handler(group_handler, events.NewMessage(pattern=fr"{hl}(promote|fullpromote|demote|ban|unban|kick|mute|unmute)", incoming=True))
    client.add_event_handler(lock_unlock_handler, events.NewMessage(pattern=fr"{hl}(lock|unlock) (\w+)", incoming=True))
    client.add_event_handler(logs_handler, events.NewMessage(pattern=fr"{hl}logs", incoming=True))
    client.add_event_handler(set_text_handler, events.NewMessage(pattern=fr"{hl}(setwelcome|setleave|setrules)(.+)?", incoming=True))
    client.add_event_handler(rules_handler, events.NewMessage(pattern=fr"{hl}rules", incoming=True))
    client.add_event_handler(welcome_leave_handler, ChatAction())
    client.add_event_handler(echo_handler, events.NewMessage(pattern=fr"{hl}echo", incoming=True))
    client.add_event_handler(rmecho_handler, events.NewMessage(pattern=fr"{hl}rmecho", incoming=True))
    client.add_event_handler(userinfo_handler, events.NewMessage(pattern=fr"{hl}userinfo(.+)?", incoming=True))
    client.add_event_handler(shutdown_handler, events.NewMessage(pattern=fr"{hl}shutdown", incoming=True))
    client.add_event_handler(start_handler, events.NewMessage(pattern=fr"{hl}start", incoming=True))
