from signal import signal, SIGINT
import random
from random import choice
from os import path as ospath, remove as osremove, execl as osexecl
from subprocess import run as srun, check_output
from datetime import datetime, timedelta
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from time import time
from sys import executable
from telegram import ParseMode, InlineKeyboardMarkup
from telegram.ext import CommandHandler
import requests
import pytz
from bot import bot, dispatcher, updater, botStartTime, TIMEZONE, IGNORE_PENDING_REQUESTS, LOGGER, Interval, INCOMPLETE_TASK_NOTIFIER, \
                    DB_URI, alive, app, main_loop, HEROKU_API_KEY, HEROKU_APP_NAME, AUTHORIZED_CHATS, EMOJI_THEME, \
                    CREDIT_NAME, TITLE_NAME, PICS, FINISHED_PROGRESS_STR, UN_FINISHED_PROGRESS_STR, \
                    SHOW_LIMITS_IN_STATS, LEECH_LIMIT, TORRENT_DIRECT_LIMIT, MEGA_LIMIT, ZIP_UNZIP_LIMIT, TOTAL_TASKS_LIMIT, USER_TASKS_LIMIT
from .helper.ext_utils.fs_utils import start_cleanup, clean_all, exit_clean_up
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.ext_utils.db_handler import DbManger
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, sendMarkup, editMessage, sendLogFile, sendPhoto
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker
from bot.modules.wayback import getRandomUserAgent
from .modules import authorize, cancel_mirror, mirror_status, mirror_leech, shell, eval, \
                    delete, leech_settings, wayback, bt_select, sleep
from datetime import datetime



def progress_bar(percentage):
    p_used = FINISHED_PROGRESS_STR
    p_total = UN_FINISHED_PROGRESS_STR
    if isinstance(percentage, str):
        return 'NaN'
    try:
        percentage=int(percentage)
    except:
        percentage = 0
    return ''.join(
        p_used if i <= percentage // 10 else p_total for i in range(1, 11)
    )

now=datetime.now(pytz.timezone(f'{TIMEZONE}'))

def stats(update, context):
    if ospath.exists('.git'):
        if EMOJI_THEME is True:
            last_commit = check_output(["git log -1 --date=short --pretty=format:'%cd \n<b>├</b> 🛠<b>From</b> %cr'"], shell=True).decode()
            botVersion = check_output(["git log -1 --date=format:v%y.%m%d.%H%M --pretty=format:%cd"], shell=True).decode()
        else:
            last_commit = check_output(["git log -1 --date=short --pretty=format:'%cd \n<b>├</b> <b>From</b> %cr'"], shell=True).decode()
            botVersion = check_output(["git log -1 --date=format:v%y.%m%d.%H%M --pretty=format:%cd"], shell=True).decode()
    else:
        botVersion = 'No UPSTREAM_REPO'
        last_commit = 'No UPSTREAM_REPO'
    currentTime = get_readable_time(time() - botStartTime)
    current = now.strftime('%m/%d %I:%M:%S %p')
    osUptime = get_readable_time(time() - boot_time())
    total, used, free, disk= disk_usage('/')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(net_io_counters().bytes_sent)
    recv = get_readable_file_size(net_io_counters().bytes_recv)
    cpuUsage = cpu_percent(interval=0.5)
    p_core = cpu_count(logical=False)
    t_core = cpu_count(logical=True)
    swap = swap_memory()
    swap_p = swap.percent
    swap_t = get_readable_file_size(swap.total)
    swap_u = get_readable_file_size(swap.used)
    memory = virtual_memory()
    mem_p = memory.percent
    mem_t = get_readable_file_size(memory.total)
    mem_a = get_readable_file_size(memory.available)
    mem_u = get_readable_file_size(memory.used)
    if EMOJI_THEME is True:
            stats = f'<b>╭─《🌐 BOT STATISTICS 🌐》</b>\n' \
                    f'<b>├ 🛠 Updated On: </b>{last_commit}\n'\
                    f'<b>├ ⌛ Uptime: </b>{currentTime}\n'\
                    f'<b>├ 🟢 OS Uptime: </b>{osUptime}\n'\
                    f'<b>├ 🖥️ CPU:</b> [{progress_bar(cpuUsage)}] {cpuUsage}%\n'\
                    f'<b>├ 🎮 RAM:</b> [{progress_bar(mem_p)}] {mem_p}%\n'\
                    f'<b>├ 💾 Disk:</b> [{progress_bar(disk)}] {disk}%\n'\
                    f'<b>├ 💿 Disk Free:</b> {free}\n'\
                    f'<b>├ 🔺 Upload Data:</b> {sent}\n'\
                    f'<b>╰ 🔻 Download Data:</b> {recv}\n\n'

    else:
            stats = f'<b>╭─《 BOT STATISTICS 》</b>\n' \
                    f'<b>├  Updated On: </b>{last_commit}\n'\
                    f'<b>├  Uptime: </b>{currentTime}\n'\
                    f'<b>├  OS Uptime: </b>{osUptime}\n'\
                    f'<b>├  CPU usage:</b> [{progress_bar(cpuUsage)}] {cpuUsage}%\n'\
                    f'<b>├  RAM:</b> [{progress_bar(mem_p)}] {mem_p}%\n'\
                    f'<b>├  Disk:</b> [{progress_bar(disk)}] {disk}%\n'\
                    f'<b>├  Disk Free:</b> {free}\n'\
                    f'<b>├  Upload Data:</b> {sent}\n'\
                    f'<b>╰  Download Data:</b> {recv}\n\n'



    if SHOW_LIMITS_IN_STATS is True:
        if TORRENT_DIRECT_LIMIT is None:
            torrent_direct = 'No Limit Set'
        else:
            torrent_direct = f'{TORRENT_DIRECT_LIMIT}GB/Link'
        if MEGA_LIMIT is None:
            mega_limit = 'No Limit Set'
        else:
            mega_limit = f'{MEGA_LIMIT}GB/Link'
        if LEECH_LIMIT is None:
            leech_limit = 'No Limit Set'
        else:
            leech_limit = f'{LEECH_LIMIT}GB/Link'
        if ZIP_UNZIP_LIMIT is None:
            zip_unzip = 'No Limit Set'
        else:
            zip_unzip = f'{ZIP_UNZIP_LIMIT}GB/Link'
        if TOTAL_TASKS_LIMIT is None:
            total_task = 'No Limit Set'
        else:
            total_task = f'{TOTAL_TASKS_LIMIT} Total Tasks/Time'
        if USER_TASKS_LIMIT is None:
            user_task = 'No Limit Set'
        else:
            user_task = f'{USER_TASKS_LIMIT} Tasks/user'


        if EMOJI_THEME is True: 
            stats += f'<b>╭─《 ⚠️ BOT LIMITS ⚠️ 》</b>\n'\
                     f'<b>├ 🧲 Torrent/Direct: </b>{torrent_direct}\n'\
                     f'<b>├ 🔐 Zip/Unzip: </b>{zip_unzip}\n'\
                     f'<b>├ 🔷 Leech: </b>{leech_limit}\n'\
                     f'<b>├ 🔰 Mega: </b>{mega_limit}\n'\
                     f'<b>├ 💣 Total Tasks: </b>{total_task}\n'\
                     f'<b>╰ 🔫 User Tasks: </b>{user_task}\n\n'
        else: 
            stats += f'<b>╭─《  BOT LIMITS  》</b>\n'\
                     f'<b>├  Torrent/Direct: </b>{torrent_direct}\n'\
                     f'<b>├  Zip/Unzip: </b>{zip_unzip}\n'\
                     f'<b>├  Leech: </b>{leech_limit}\n'\
                     f'<b>├  Mega: </b>{mega_limit}\n'\
                     f'<b>├  Total Tasks: </b>{total_task}\n'\
                     f'<b>╰  User Tasks: </b>{user_task}\n\n'

                


def start(update, context):
    buttons = ButtonMaker()
    buttons.buildbutton("PublicLeechCloneGroup", "https://t.me/PublicLeechCloneGroup")
    reply_markup = InlineKeyboardMarkup(buttons.build_menu(2))
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
Welcome | BOT is ready for you
Type /{BotCommands.HelpCommand} to get a list of available commands
'''
        sendMarkup(start_string, context.bot, update.message, reply_markup)
    else:
        sendMarkup('Sorry, You cannot use me', context.bot, update.message, reply_markup)


def restart(update, context):
    restart_message = sendMessage("Restarting...", context.bot, update.message)
    if Interval:
        Interval[0].cancel()
        Interval.clear()
    alive.kill()
    clean_all()
    srun(["pkill", "-9", "-f", "gunicorn|chrome|firefox|megasdkrest|opera"])
    srun(["python3", "update.py"])
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    osexecl(executable, executable, "-m", "bot")





def log(update, context):
    sendLogFile(context.bot, update.message)


help_string = f'''
/{BotCommands.LeechCommand}: Start leeching to Telegram.

/{BotCommands.ZipLeechCommand}: Start leeching and upload the file/folder compressed with zip extension.

/{BotCommands.UnzipLeechCommand}: Start leeching and upload the file/folder extracted from any archive extension.

/{BotCommands.QbLeechCommand}: Start leeching using qBittorrent.

/{BotCommands.QbZipLeechCommand}: Start leeching using qBittorrent and upload the file/folder compressed with zip extension.

/{BotCommands.QbUnzipLeechCommand}: Start leeching using qBittorrent and upload the file/folder extracted from any archive extension.

/{BotCommands.LeechSetCommand} [query]: Leech settings.

/{BotCommands.SetThumbCommand}: Reply photo to set it as Thumbnail.

/{BotCommands.BtSelectCommand}: Select files from torrents by gid or reply.

/{BotCommands.CancelMirror}: Cancel task by gid or reply.

/{BotCommands.StatusCommand}: Shows a status of all the downloads.

/{BotCommands.StatsCommand}: Show stats of the machine where the bot is hosted in.

'''

def bot_help(update, context):
    sendMessage(help_string, context.bot, update.message)


def main():
    start_cleanup()
    date = now.strftime('%d/%m/%y')
    time = now.strftime('%I:%M:%S %p')
    notifier_dict = False
    if INCOMPLETE_TASK_NOTIFIER and DB_URI is not None:
        if notifier_dict := DbManger().get_incomplete_tasks():
            for cid, data in notifier_dict.items():
                if ospath.isfile(".restartmsg"):
                    with open(".restartmsg") as f:
                        chat_id, msg_id = map(int, f)
                    msg = f"Restarted successfully❗\n"
                    msg += f" DATE: {date}\n"
                    msg += f" TIME: {time}\n"
                    msg += f" TIMEZONE: {TIMEZONE}\n"
                else:
                    msg = f"Bot Restarted!\n"
                    msg += f"DATE: {date}\n"
                    msg += f"TIME: {time}\n"
                    msg += f"TIMEZONE: {TIMEZONE}"

                for tag, links in data.items():
                     msg += f"\n{tag}: "
                     for index, link in enumerate(links, start=1):
                         msg += f" <a href='{link}'>{index}</a> |"
                         if len(msg.encode()) > 4000:
                             if 'Restarted successfully' in msg and cid == chat_id:
                                 bot.editMessageText(msg, chat_id, msg_id, parse_mode='HTML', disable_web_page_preview=True)
                                 osremove(".restartmsg")
                             else:
                                 try:
                                     bot.sendMessage(cid, msg, 'HTML', disable_web_page_preview=True)
                                 except Exception as e:
                                     LOGGER.error(e)
                             msg = ''
                if 'Restarted successfully' in msg and cid == chat_id:
                     bot.editMessageText(msg, chat_id, msg_id, parse_mode='HTML', disable_web_page_preview=True)
                     osremove(".restartmsg")
                else:
                    try:
                        bot.sendMessage(cid, msg, 'HTML', disable_web_page_preview=True)
                    except Exception as e:
                        LOGGER.error(e)

    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        msg = f"Restarted successfully\n DATE: {date}\n TIME: {time}\n TIMEZONE: {TIMEZONE}\n"
        bot.edit_message_text(msg, chat_id, msg_id)
        osremove(".restartmsg")
    elif not notifier_dict and AUTHORIZED_CHATS:
        text = f" Bot Restarted! \nDATE: {date} \nTIME: {time} \nTIMEZONE: {TIMEZONE}"
        for id_ in AUTHORIZED_CHATS:
            try:
                bot.sendMessage(chat_id=id_, text=text, parse_mode=ParseMode.HTML)
            except Exception as e:
                LOGGER.error(e)


    start_handler = CommandHandler(BotCommands.StartCommand, start, run_async=True)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                     filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    help_handler = CommandHandler(BotCommands.HelpCommand,
                                  bot_help, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    stats_handler = CommandHandler(BotCommands.StatsCommand,
                                   stats, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user, run_async=True)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter | CustomFilters.sudo_user, run_async=True)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(log_handler)
    updater.start_polling(drop_pending_updates=IGNORE_PENDING_REQUESTS)
    LOGGER.info("💥𝐁𝐨𝐭 𝐒𝐭𝐚𝐫𝐭𝐞𝐝❗")
    signal(SIGINT, exit_clean_up)

app.start()
main()

main_loop.run_forever()
