from bot import CMD_INDEX
import os
def getCommand(name: str, command: str):
    try:
        if len(os.environ[name]) == 0:
            raise KeyError
        return os.environ[name]
    except KeyError:
        return command


class _BotCommands:
    def __init__(self):
        self.StartCommand = getCommand(f'START_COMMAND', f'start{CMD_INDEX}')
        self.MirrorCommand = getCommand(f'MIRROR_COMMAND', f'mirror{CMD_INDEX}')
        self.CancelMirror = getCommand('CANCEL_COMMAND', f'cancel{CMD_INDEX}')
        self.CancelAllCommand = getCommand('CANCEL_ALL_COMMAND', f'cancelall{CMD_INDEX}')
        self.StatusCommand = getCommand('STATUS_COMMAND', f'status{CMD_INDEX}')
        self.AuthorizedUsersCommand = getCommand('USERS_COMMAND', f'users{CMD_INDEX}')
        self.AuthorizeCommand = getCommand('AUTH_COMMAND', f'authorize{CMD_INDEX}')
        self.UnAuthorizeCommand = getCommand('UNAUTH_COMMAND', f'unauthorize{CMD_INDEX}')
        self.AddSudoCommand = getCommand('ADDSUDO_COMMAND', f'addsudo{CMD_INDEX}')
        self.RmSudoCommand = getCommand('RMSUDO_COMMAND', f'rmsudo{CMD_INDEX}')
        self.RestartCommand =  getCommand('RESTART_COMMAND', f'restart{CMD_INDEX}')
        self.StatsCommand = f'stats{CMD_INDEX}'
        self.HelpCommand = getCommand('HELP_COMMAND', f'help{CMD_INDEX}')
        self.LogCommand = getCommand('LOG_COMMAND', f'log{CMD_INDEX}')
        self.BtSelectCommand = getCommand('BTSEL_COMMAND', f'btsel{CMD_INDEX}')
        self.DeleteCommand = getCommand('DELETE_COMMAND', f'del{CMD_INDEX}')
        self.ShellCommand = getCommand('SHELL_COMMAND', f'shell{CMD_INDEX}')
        self.ExecHelpCommand = getCommand('EXEHELP_COMMAND', f'exechelp{CMD_INDEX}')
        self.LeechSetCommand = getCommand('LEECHSET_COMMAND', f'leechset{CMD_INDEX}')
        self.SetThumbCommand = getCommand('SETTHUMB_COMMAND', f'setthumb{CMD_INDEX}')
        self.LeechCommand = getCommand('LEECH_COMMAND', f'leech{CMD_INDEX}')
        self.UnzipLeechCommand = getCommand('UNZIPLEECH_COMMAND', f'unzipleech{CMD_INDEX}')
        self.ZipLeechCommand = getCommand('ZIPLEECH_COMMAND', f'zipleech{CMD_INDEX}')
        self.QbLeechCommand = getCommand('QBLEECH_COMMAND', f'qbleech{CMD_INDEX}')
        self.QbUnzipLeechCommand = getCommand('QBZIPLEECH_COMMAND', f'qbunzipleech{CMD_INDEX}')
        self.QbZipLeechCommand = getCommand('QBUNZIPLEECH_COMMAND', f'qbzipleech{CMD_INDEX}')
        self.WayBackCommand = getCommand('WAYBACK_COMMAND', f'wayback{CMD_INDEX}')
        self.SleepCommand = getCommand('SLEEP_COMMAND', f'sleep{CMD_INDEX}')
        self.AddleechlogCommand = getCommand('ADDLEECHLOG_CMD', f'addleechlog{CMD_INDEX}')
        self.RmleechlogCommand = getCommand('RMLEECHLOG_CMD', f'rmleechlog{CMD_INDEX}')
        self.EvalCommand = f'eval{CMD_INDEX}'
        self.ExecCommand = f'exec{CMD_INDEX}'
        self.ClearLocalsCommand = f'clearlocals{CMD_INDEX}'

BotCommands = _BotCommands()
