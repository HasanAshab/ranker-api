from django.conf import settings
from django.core import management
from django.core.management.base import (
    BaseCommand,
)
from django.utils import timezone
from command_scheduler.enums import ScheduleType


class Command(BaseCommand):
    help = "Run scheduled commands"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        for command_config in settings.SCHEDULED_COMMANDS:
            if not command_config.get("enabled", True):
                return
            if command_config["schedule"] == ScheduleType.DAILY:
                self._call_command(command_config)

            if (
                command_config["schedule"] == ScheduleType.WEEKLY
                and now.weekday() == 0
            ):
                self._call_command(command_config)

            if (
                command_config["schedule"] == ScheduleType.MONTHLY
                and now.day == 1
            ):
                self._call_command(command_config)

    def _call_command(self, command_config):
        command_name = command_config["command"]
        args = command_config.get("args", {})
        positional_args = args.get("args", [])
        optional_args = args.get("options", {})
        management.call_command(
            command_name, *positional_args, **optional_args
        )
