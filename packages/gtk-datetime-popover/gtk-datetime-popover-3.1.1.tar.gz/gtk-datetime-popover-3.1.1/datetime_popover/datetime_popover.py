#!/usr/bin/env python3
"""
Name: gtk-datetime-popover

Description: This datetime popover allows for the

Usage

License

# todo add module level docstrings
"""

import pathlib
from datetime import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# todo update test cases


# Helper functions #####################################################################################################
def _enlarge_spinbox_font(spinbox):
    """Increases the font size of the provided gtk spinbox by 400%."""
    css = b'''spinbutton {font-size: 400%;}'''
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css)
    spinbox_style_context = spinbox.get_style_context()
    spinbox_style_context.add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)


def _show_leading_zeros(spinbox):
    """Adds leading zeros to the given gtk spinbox"""
    adjustment = spinbox.get_adjustment()
    value = int(adjustment.get_value())
    spinbox.set_text(f'{value:02d}')
    return True


# DateTimePicker Class ################################################################################################
class DateTimePicker:
    """The main logic class for the datetime picker."""
    def __init__(self):
        # todo add method and function docstrings

        # gtk builder setup
        glade_file_path = str(pathlib.Path(__file__).resolve().parent / "datetime_popover.glade")
        gtk_builder = Gtk.Builder()
        gtk_builder.add_from_file(glade_file_path)
        gtk_builder.connect_signals(self)
        # Widget Fetching
        self._popover = gtk_builder.get_object('popover')
        self._stack_switcher = gtk_builder.get_object('stack_switcher')
        self._stack = gtk_builder.get_object('stack')
        self._calendar = gtk_builder.get_object('calendar')
        self._current_date_button = gtk_builder.get_object('current_date_button')
        self._clear_date_button = gtk_builder.get_object('clear_date_button')
        self._outer_time_grid = gtk_builder.get_object('outer_time_grid')
        self._hour_spinbox = gtk_builder.get_object('hour_spinbox')
        self._minute_spinbox = gtk_builder.get_object('minute_spinbox')
        self._clear_time_button = gtk_builder.get_object('clear_time_button')
        self._current_time_button = gtk_builder.get_object('current_time_button')
        # Spinbox setup
        for spinbox in [self._hour_spinbox, self._minute_spinbox]:
            _enlarge_spinbox_font(spinbox)
            spinbox.connect('output', _show_leading_zeros)
        # date initialization
        self.datetime = None

    # element handlers -------------------------------------------------------------------------------------------------
    def _on_calendar_day_selected(self, *_):
        # todo add method and function docstrings
        self._update_clear_date_button()
        self._update_time_visibility()

    def _on_time_spinboxes_changed(self, *_):
        # todo add method and function docstrings
        self._update_clear_time_button()

    def _on_current_date_button_clicked(self, *_):
        # todo add method and function docstrings
        self.select_current_date()

    def _on_clear_date_button_clicked(self, *_):
        # todo add method and function docstrings
        self.clear_date()

    def _on_current_time_button_clicked(self, *_):
        # todo add method and function docstrings
        self.select_current_time()

    def _on_clear_time_button_clicked(self, *_):
        # todo add method and function docstrings
        self.clear_time()

    #  Update Methods --------------------------------------------------------------------------------------------------
    def _update_clear_date_button(self):
        # todo add method and function docstrings
        """This handler enables and disables the clear date button, depending on whether a day is selected or not"""
        self._clear_date_button.set_sensitive(True if self.day else False)

    def _update_clear_time_button(self):
        # todo add method and function docstrings
        """This method updates the clear time button depending on whether the hour and minute spinboxes are set to 0"""
        hour = self._hour_spinbox.get_value_as_int()
        minute = self._minute_spinbox.get_value_as_int()
        sensitive = True if hour or minute else False
        self._clear_time_button.set_sensitive(sensitive)

    def _update_time_visibility(self):
        # todo add method and function docstrings
        self._stack_switcher.set_sensitive(bool(self.day))

    # popover methods --------------------------------------------------------------------------------------------------
    def raise_popover(self):
        # todo add method and function docstrings

        """This raises the popup"""

        self._popover.popup()
        self._popover.show_all()

    def set_relative_to(self, widget):
        # todo add method and function docstrings

        self._popover.set_relative_to(widget)

    def connect_popover_closed_signal(self, function):
        # todo add method and function docstrings

        self._popover.connect('closed', function)

    # Changed handler conncetion ---------------------------------------------------------------------------------------
    def connect_changed_signal(self, function):
        # todo add method and function docstrings

        self._calendar.connect('day-selected', function)
        self._hour_spinbox.connect('value-changed', function)
        self._minute_spinbox.connect('value-changed', function)

    #  Selection Functions ---------------------------------------------------------------------------------------------
    def select_current_date(self):
        # todo add method and function docstrings

        """Sets the calendar to the current date. The time picker is not affected"""
        current_date = datetime.now()
        self.year = current_date.year
        self.month = current_date.month
        self.day = current_date.day

    def clear_date(self):
        # todo add method and function docstrings
        """This sets the day to 0, clearing the date for the gtk widget"""
        self.select_current_date()
        self.day = 0

    def select_current_time(self):
        # todo add method and function docstrings

        """This handler sets the hour and minute spinboxes to the current time. The date is not affected"""
        current_time = datetime.now()
        self.hour = current_time.hour
        self.minute = current_time.minute

    def clear_time(self):
        # todo add method and function docstrings

        """This handler clears the hour and minute spinboxes by setting both to 0. The date is not affected"""
        self.hour = 0
        self.minute = 0

    # datetime properties ----------------------------------------------------------------------------------------------
    @property
    def year(self):

        # todo add method and function docstrings
        return self._calendar.get_date().year

    @year.setter
    def year(self, year):
        # todo add method and function docstrings

        self._calendar.select_month(self.month - 1, year)

    @property
    def month(self):
        # todo add method and function docstrings
        return self._calendar.get_date().month + 1

    @month.setter
    def month(self, month):
        # todo add method and function docstrings
        self._calendar.select_month(month - 1, self.year)

    @property
    def day(self):
        # todo add method and function docstrings
        return self._calendar.get_date().day

    @day.setter
    def day(self, day):
        # todo add method and function docstrings
        self._calendar.select_day(day)
        self._update_clear_date_button()

    @property
    def hour(self):
        # todo add method and function docstrings
        return self._hour_spinbox.get_value_as_int()

    @hour.setter
    def hour(self, hour):
        # todo add method and function docstrings
        self._hour_spinbox.set_value(hour)
        self._update_clear_time_button()

    @property
    def minute(self):
        # todo add method and function docstrings
        return self._minute_spinbox.get_value_as_int()

    @minute.setter
    def minute(self, minute):
        # todo add method and function docstrings
        self._minute_spinbox.set_value(minute)
        self._update_clear_time_button()

    @property
    def datetime(self):
        # todo add method and function docstrings
        if self._calendar.get_date().day:
            return datetime(self.year, self.month, self.day, self.hour, self.minute)

    @datetime.setter
    def datetime(self, datetime_object):
        # todo add method and function docstrings
        if datetime_object:
            self.year = datetime_object.year
            self.month = datetime_object.month
            self.day = datetime_object.day
            self.hour = datetime_object.hour
            self.minute = datetime_object.minute
        else:
            self.clear_date()
            self.clear_time()


class DateTimeButton:
    def __init__(
            self, date_format_string='%Y-%m-%d', datetime_format_string='%Y-%m-%d at %H:%M',
            no_date_string='Select Date'):
        # todo add method and function docstrings
        """
        :param date_format_string:
        :param datetime_format_string:
        :param no_date_string:
        """
        self.date_format_string = date_format_string
        self.datetime_format_string = datetime_format_string
        self.no_date_string = no_date_string
        self.button = Gtk.Button()
        self.picker = DateTimePicker()

        self.button.connect('clicked', self._on_button_clicked)
        self.picker.set_relative_to(self.button)
        self.picker.connect_popover_closed_signal(self._on_popover_closed)
        self.picker.connect_changed_signal(self._on_datetime_changed)
        self.set_date_button_label()

    def _on_button_clicked(self, *_):
        # todo add method and function docstrings
        self.picker.raise_popover()

    def _on_popover_closed(self, *_):
        # todo add method and function docstrings
        self.set_date_button_label()

    def _on_datetime_changed(self, *_):
        # todo add method and function docstrings
        self.set_date_button_label()

    def set_date_button_label(self):
        # todo add method and function docstrings
        if self.picker.datetime:
            use_datetime_format_string = (self.picker.minute or self.picker.hour) and self.datetime_format_string
            format_string = self.datetime_format_string if use_datetime_format_string else self.date_format_string
            final_date_string = self.picker.datetime.strftime(format_string)
            self.button.set_label(final_date_string)
        else:
            self.button.set_label(self.no_date_string)
