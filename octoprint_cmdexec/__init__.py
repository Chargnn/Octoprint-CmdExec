# coding=utf-8

import octoprint.plugin
from flask import make_response
from . import cli
import subprocess

from octoprint.access.permissions import Permissions

class CmdExecPlugin(octoprint.plugin.StartupPlugin,
                    octoprint.plugin.TemplatePlugin,
                    octoprint.plugin.SettingsPlugin,
                    octoprint.plugin.AssetPlugin,
                    octoprint.plugin.SimpleApiPlugin):

    def get_settings_defaults(self):
        return dict(
            command=""
        )

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]

    def get_api_commands(self):
        return dict(
            execute=[]
        )

    def execute(self):
        subprocess.Popen(self._settings.get(["command"]), shell=True)

    def on_api_command(self, command, data):
        if not Permissions.ADMIN.can():
            return make_response("Insufficient rights", 403)

        if command == "execute":
            self.execute()
        pass

    def get_assets(self):
        return {
            "js": ["js/cmdexec.js"]
        }

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

    def on_after_startup(self):
        command = self._settings.get(["command"])

    def get_update_information(self):
        return dict(
            cmdexec=dict(
                displayName="CMD Exec",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="Chargnn",
                repo="Octoprint-CmdExec",
                current=self._plugin_version,

                # update method: pip w/ dependency links
                pip="https://github.com/Chargnn/Octoprint-CmdExec/archive/refs/tags/{target_version}.zip"
            )
        )

__plugin_name__ = "CMD Exec"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = CmdExecPlugin()
__plugin__hook__ = {
        "octoprint.cli.commands": cli.commands
}