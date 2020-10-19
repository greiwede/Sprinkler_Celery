from django.db import models
from django.forms import ModelForm
from django import forms
import datetime

# Status Choices for Plans & Devices
STATUS_CHOICES = [
    ('OK', 'OK'),
    ('Warnung', 'Warnung'),
    ('Fehler', 'Fehler'),
]


class CommonInfo(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='OK',
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Device(CommonInfo):
    contr_id = models.IntegerField()
    device_type = None

    class Meta:
        abstract = True


# Pump Model
class Pump(Device):
    curr_active = models.BooleanField(default=False)
    device_type = 'Pump'
    flow_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    current_workload = models.DecimalField(max_digits=5, decimal_places=2)


class PumpForm(ModelForm):
    class Meta:
        model = Pump
        fields = ('name', 'status')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class Sensor(Device):
    curr_active = models.BooleanField(default=False)
    device_type = 'Sensor'
    moisture = None
    moisture_threshold = models.DecimalField(max_digits=5, decimal_places=2)


class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        fields = ('name', 'status')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class Valve(Device):
    curr_active = models.BooleanField(default=False)
    device_type = 'Ventil'
    valve_counter = None
    valve_threshold = models.IntegerField(default=100)
    sensor_fk = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True)
    pump_fk = models.ForeignKey(Pump, on_delete=models.SET_NULL, null=True)


# Sprinkler Model
class Sprinkler(Device):
    curr_active = models.BooleanField(default=False)
    device_type = 'Sprinkler'
    flow_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    valve_fk = models.ForeignKey(Valve, on_delete=models.SET_NULL, null=True)  # Sprenkler weiterhin gespeichert, wenn ein Ventil geloescht wird, damit es bei Bedarf einen anderen Ventil zugeordnet werden kann


# Form for Sprinkler
class SprinklerForm(ModelForm):
    class Meta:
        model = Sprinkler
        fields = ('name', 'status')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class Plan(CommonInfo):
    description = models.CharField(max_length=3000, default="Beschreibung")

    automation_rain = models.BooleanField(default=False)
    timespace_rain_forecast = models.IntegerField(default=24) # Standardwert 24h Forecast beachten
    automation_sensor = models.BooleanField(default=False)
    # evt. noch 3. Moeglichkeit hinzufuegen

    # Relationen zu Ventilen
    valve = models.ManyToManyField(Valve)

    next_execution_time = None

    def get_related_schedules(self):
        return self.schedule_set.all()

    def get_related_pumps(self):
        return self.pump.all()

    def is_current_time_denied(self):
        return True

    def get_next_allowed_start_date_time(self):
        next_allowed_start_date_time = None
        schedules = self.get_related_schedules()
        for schedule in schedules:
            schedule_next_allowed_date_time = schedule.get_next_date_time(schedule.get_allowed_weekdays(),
                                                                          schedule.allow_time_start)
            if (next_allowed_start_date_time == None) or (
                    next_allowed_start_date_time > schedule_next_allowed_date_time):
                next_allowed_start_date_time = schedule_next_allowed_date_time
        return next_allowed_start_date_time

    def get_next_denied_start_date_time(self):
        next_denied_start_date_time = None
        schedules = self.get_related_schedules()
        for schedule in schedules:
            schedule_next_denied_start_date_time = schedule.get_next_date_time(schedule.get_denied_weekdays(),
                                                                               schedule.deny_time_start)
            if (next_denied_start_date_time == None) or (
                    next_denied_start_date_time > schedule_next_denied_start_date_time):
                next_denied_start_date_time = schedule_next_denied_start_date_time
        return next_denied_start_date_time

    def get_next_allowed_end_date_time(self):
        next_allowed_start_date_time = None
        schedules = self.get_related_schedules()
        for schedule in schedules:
            schedule_next_allowed_date_time = schedule.get_next_date_time(schedule.get_allowed_weekdays(),
                                                                          schedule.allow_time_stop)
            if (next_allowed_start_date_time == None) or (
                    next_allowed_start_date_time > schedule_next_allowed_date_time):
                next_allowed_start_date_time = schedule_next_allowed_date_time
        return next_allowed_start_date_time

    def get_next_denied_end_date_time(self):
        next_denied_start_date_time = None
        schedules = self.get_related_schedules()
        for schedule in schedules:
            schedule_next_denied_start_date_time = schedule.get_next_date_time(schedule.get_denied_weekdays(),
                                                                               schedule.deny_time_stop)
            if (next_denied_start_date_time == None) or (
                    next_denied_start_date_time > schedule_next_denied_start_date_time):
                next_denied_start_date_time = schedule_next_denied_start_date_time
        return next_denied_start_date_time

    def get_pumps_to_be_activated(self):
        schedules = self.get_related_schedules()
        pumps_to_be_activated = None
        is_denied_time = False
        for schedule in schedules:
            if schedule.is_denied_time():
                return None
            elif schedule.is_allowed_time():
                pumps_to_be_activated = self.get_related_pumps()
        return pumps_to_be_activated


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ('name', 'status', 'description', 'valve')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'sprinkler': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'pump': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'sensor': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class Schedule(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    allow_monday = models.BooleanField(default=False)
    allow_tuesday = models.BooleanField(default=False)
    allow_wednesday = models.BooleanField(default=False)
    allow_thursday = models.BooleanField(default=False)
    allow_friday = models.BooleanField(default=False)
    allow_saturday = models.BooleanField(default=False)
    allow_sunday = models.BooleanField(default=False)
    allow_time_start = models.TimeField(auto_now=False, auto_now_add=False)
    allow_time_stop = models.TimeField(auto_now=False, auto_now_add=False)

    deny_monday = models.BooleanField(default=False)
    deny_tuesday = models.BooleanField(default=False)
    deny_wednesday = models.BooleanField(default=False)
    deny_thursday = models.BooleanField(default=False)
    deny_friday = models.BooleanField(default=False)
    deny_saturday = models.BooleanField(default=False)
    deny_sunday = models.BooleanField(default=False)
    deny_time_start = models.TimeField(auto_now=False, auto_now_add=False)
    deny_time_stop = models.TimeField(auto_now=False, auto_now_add=False)

    allowed_weekdays = None
    denied_weekdays = None
    next_allowed_start_date_time = None
    next_allowed_end_date_time = None
    next_denied_start_date_time = None
    next_denied_end_date_time = None

    def get_next_date_time(self, weekdays, dt):
        weekday = datetime.datetime.now().weekday()

        for i in range(0, 8):
            if weekday in weekdays:
                now_date_time = datetime.datetime.now()
                temp_date_time = now_date_time + datetime.timedelta(days=i)

                day = str("{:02d}".format(temp_date_time.day))
                month = str("{:02d}".format(temp_date_time.month))
                year = str(temp_date_time.year)
                hour = str("{:02d}".format(dt.hour))
                minute = str("{:02d}".format(dt.minute))
                second = str("{:02d}".format(dt.second))

                date_time_str = year + '-' + month + '-' + day + ' ' + hour + ':' + minute + ':' + second
                date_time = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

                if date_time > now_date_time:
                    return date_time

            if weekday == 6:
                weekday = 0
            else:
                weekday += 1

    def get_allowed_weekdays(self):
        allowed_weekdays = []
        if self.allow_monday: allowed_weekdays.append(0)
        if self.allow_tuesday: allowed_weekdays.append(1)
        if self.allow_wednesday: allowed_weekdays.append(2)
        if self.allow_thursday: allowed_weekdays.append(3)
        if self.allow_friday: allowed_weekdays.append(4)
        if self.allow_saturday: allowed_weekdays.append(5)
        if self.allow_sunday: allowed_weekdays.append(6)
        return allowed_weekdays

    def get_denied_weekdays(self):
        denied_weekdays = []
        if self.deny_monday: denied_weekdays.append(0)
        if self.deny_tuesday: denied_weekdays.append(1)
        if self.deny_wednesday: denied_weekdays.append(2)
        if self.deny_thursday: denied_weekdays.append(3)
        if self.deny_friday: denied_weekdays.append(4)
        if self.deny_saturday: denied_weekdays.append(5)
        if self.deny_sunday: denied_weekdays.append(6)
        return denied_weekdays

    def is_allowed_time(self):
        next_allowed_start_date_time = self.get_next_date_time(self.get_allowed_weekdays(), self.allow_time_start)
        next_allowed_end_date_time = self.get_next_date_time(self.get_allowed_weekdays(), self.allow_time_stop)
        if next_allowed_start_date_time != None:
            is_same_day = next_allowed_start_date_time <= next_allowed_end_date_time
        else:
            return False

        if is_same_day:
            return False
        else:
            return True

    def is_denied_time(self):
        next_denied_start_date_time = self.get_next_date_time(self.get_denied_weekdays(), self.deny_time_start)
        next_denied_end_date_time = self.get_next_date_time(self.get_denied_weekdays(), self.deny_time_stop)
        if next_denied_start_date_time != None:
            is_same_day = next_denied_start_date_time <= next_denied_end_date_time
        else:
            return False

        if is_same_day:
            return False
        else:
            return True


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = ('plan', 'allow_monday', 'allow_tuesday', 'allow_wednesday', 'allow_thursday',
                  'allow_friday', 'allow_saturday', 'allow_sunday', 'allow_time_start', 'allow_time_stop',
                  'deny_monday', 'deny_tuesday', 'deny_wednesday', 'deny_thursday',
                  'deny_friday', 'deny_saturday', 'deny_sunday', 'deny_time_start', 'deny_time_stop')

        widgets = {
            'plan': forms.NumberInput(attrs={'style': 'display:none'}),
            'allow_monday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'allow_tuesday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'allow_wednesday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'allow_thursday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'allow_friday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'allow_saturday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'allow_sunday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'allow_time_start': forms.TimeInput(attrs={'class': 'form-control'}),
            'allow_time_stop': forms.TimeInput(attrs={'class': 'form-control'}),
            'deny_monday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'deny_tuesday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'deny_wednesday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'deny_thursday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'deny_friday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'deny_saturday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'deny_sunday': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'deny_time_start': forms.TimeInput(attrs={'class': 'form-control'}),
            'deny_time_stop': forms.TimeInput(attrs={'class': 'form-control'}),
        }