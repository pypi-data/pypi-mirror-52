from datetime import datetime
from datetime import timedelta

from pony import orm

from .enums import EventStatus
from .enums import OptType
from .enums import ReportStatus


db = orm.Database()


class Event(db.Entity):
    event_id = orm.Required(str)

    # This is the start time as specified by the VTN
    official_start = orm.Required(datetime)

    # If larger than 0, this is the largest amount of randomisation we can (must) apply
    # to official_start to get start_time (below).  This is stored in start_offset.
    #
    # If 0, no randomisation is applied and start_time == official_time.
    start_after = orm.Required(timedelta)

    # This is how long the event lasts
    duration = orm.Optional(timedelta)

    # This is our calculated random offset.
    # 0 ≤ start_offset ≤ start_after
    start_offset = orm.Required(timedelta)

    # start_time = official_start + start_offset (precalculated for efficiency)
    start_time = orm.Required(datetime)

    # end_time = start_time + duration (precalculated for efficiency)
    end_time = orm.Optional(datetime)

    request_id = orm.Optional(str, nullable=True)
    created = orm.Required(datetime, default=datetime.now())
    signals = orm.Optional(str)
    status = orm.Required(str, default=EventStatus.UNRESPONDED.value)
    opt_type = orm.Optional(str, default=OptType.NONE.value)
    priority = orm.Optional(int)
    modification_number = orm.Required(int, default=0)
    test_event = orm.Required(bool, default=False)

    def __str__(self):
        """Format the instance as a string suitable for trace display."""
        event_string = f"{self.__class__.__name__}: "
        event_string += f"event_id:{self.event_id}; "
        event_string += f"start_time:{self.start_time}; "
        event_string += f"end_time:{self.end_time}; "
        event_string += f"request_id:{self.request_id}; "
        event_string += f"status:{self.status}; "
        event_string += f"opt_type: {self.opt_type};"
        event_string += f"priority:{self.priority}; "
        event_string += f"modification_number:{self.modification_number}; "
        event_string += f"signals:{self.signals}; "
        return event_string

    @property
    def is_active_or_pending(self):
        return self.status not in [
            EventStatus.COMPLETED.value,
            EventStatus.CANCELED.value,
        ]


class Report(db.Entity):
    start_time = orm.Required(datetime)
    end_time = orm.Required(datetime)
    duration = orm.Required(timedelta)
    last_report_time = orm.Required(datetime)
    name = orm.Required(str)
    interval_secs = orm.Required(int, default=0)
    granularity_secs = orm.Optional(str, default="")
    telemetry_parameters = orm.Optional(str)
    created = orm.Required(datetime, default=datetime.now())
    request_id = orm.Required(str)
    specifier_id = orm.Required(str)
    status = orm.Required(str, default=ReportStatus.INACTIVE.value)
    last_report = orm.Required(datetime, default=datetime.now())

    @property
    def is_active_or_pending(self):
        return self.status not in [
            ReportStatus.STATUS_COMPLETED,
            ReportStatus.STATUS_CANCELED,
        ]


class TelemetryValues(db.Entity):
    """Model object for telemetry values."""

    created = orm.Required(datetime, default=datetime.now())
    report_request_id = orm.Required(str)
    baseline_power_kw = orm.Optional(float)
    current_power_kw = orm.Optional(float)
    start_time = orm.Optional(datetime)
    end_time = orm.Optional(datetime)

    def __str__(self):
        """Format the instance as a string suitable for trace display."""
        tel_string = f"{self.__class__.__name__}: "
        tel_string += f"created_on:{self.created}; "
        tel_string += f"report_request_id:{self.report_request_id}; "
        tel_string += f"baseline_power_kw:{self.baseline_power_kw}; "
        tel_string += f"current_power_kw:{self.current_power_kw} "
        tel_string += f"start_time:{self.start_time} "
        tel_string += f"end_time:{self.end_time} "
        return tel_string

    @property
    def duration(self):
        return self.end_time - self.start_time


def setup_db(filepath=None):
    if filepath:
        db.bind(provider="sqlite", filename=filepath, create_db=True)
    else:
        db.bind(provider="sqlite", filename=":memory:", create_db=True)
    db.generate_mapping(create_tables=True)
