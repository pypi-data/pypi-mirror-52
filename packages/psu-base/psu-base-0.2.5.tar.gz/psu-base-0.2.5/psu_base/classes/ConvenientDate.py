from django.conf import settings
from psu_base.services import date_service
from psu_base.classes.Log import Log
import arrow
import datetime

log = Log()


class ConvenientDate:
    # The user-entered value
    original_value = None

    # A datetime object to to used as you see fit
    datetime_instance = None

    # An Arrow object to be used as you see fit
    # https://arrow.readthedocs.io/en/latest/
    arrow_instance = None

    def date_field(self):
        """Date to be used as value="" in a date input"""
        return self.format("YYYY-MM-DD")

    def timestamp(self):
        """Unambiguous date string to the second"""
        return self.format("YYYY-MM-DD HH:mm:ss")

    def banner_date(self):
        """The format Banner users expect to see"""
        return self.format("DD-MMM-YYYY").upper()

    def banner_date_time(self):
        """The format Banner users expect to see"""
        return self.format("DD-MMM-YYYY HH:mm").upper()

    def humanized(self, compared_to="now", granularity="auto"):
        """
        A vague description of a date/time
        granularity: ["second", "minute", "hour", "day", "week", "month" or "year"]
        """
        if self.arrow_instance:
            return self.arrow_instance.humanize(
                ConvenientDate(compared_to).arrow_instance,
                granularity=granularity
            )
        else:
            return ''

    def format(self, format_string="MMMM DD, YYYY"):
        """
        Format a date using Arrow's formatting patterns, which are more intuitive
        https://arrow.readthedocs.io/en/latest/
        """
        if self.arrow_instance:
            return self.arrow_instance.format(format_string)
        else:
            return ""

    def __init__(self, date_string):
        if date_string:
            self.original_value = date_string

            # Convert the date string to a datetime instance
            if str(date_string).lower() == 'now':
                self.datetime_instance = datetime.datetime.now()
            else:
                self.datetime_instance = date_service.string_to_date(date_string)

            self.arrow_instance = arrow.get(self.datetime_instance)

    def __str__(self):
        return self.humanized()
