from __future__ import absolute_import, unicode_literals

from datetime import date

from celery import shared_task

from .models import *
import time # test


#test
@shared_task
def add(a,b):
    time.sleep(5)
    return a+b

#test
@shared_task
def print_test():
    print('test')

@shared_task
def aut_irrigation():
    # ist Sprengzeit erlaubt
    if time_allowed: #Abfrage an Model
        # mit Bodensensor
        if is_sensor_activ: # Abfrage an MC
            # alle Sensor-IDs aus DB abrufen
            sensor_list = get_sensor_list()
            # Schleife - alle Sensoren durchgehen
            for sensor in sensor_list:
                # Methode zur Wassermengenberechnung für den jeweiligen Sensor aufrufen
                wateramount = calculate_water_amount_sensor(sensor.pk)
                # Alle Ventile, die dem entsprechenden Sensor zugeornet sind in ventil_list speichern
                ventil_list = get_valve_sensor_list(sensor)
                # jeden Ventil die Wassermenge zuweisen
                for ventil in ventil_list:
                    set_water_amount_ventil(ventil.pk, wateramount)
        else:
            # alle Ventil-IDs aus DB abrufen
            ventil_list = get_valve_list()
            # Schleife - alle Ventile durchgehen
            current_weather_counter = 1
            for ventil in ventil_list:
                # Addiere Wetterzaehler zu jeden Ventilzaehler
                add_weathercounter_to_ventilcounter(ventil.pk, current_weather_counter)
            #weather_counter.reset_current_weather_counter(maria_db_connection)
            calculate_water_amount_valve()

            # Wassermenge > 0 bei mindestens einem Ventil?
        if get_highest_wateramount_ventil > 0:
            # berechne zu sprengende Zeit
            ventil_wateramount_list = get_wateramount_valves()
            ventil_water_per_minute_list = get_ventils_water_per_minute()
            i = 0
            for row in ventil_wateramount_list:
                Valve[i] = ventil_wateramount_list[i] / ventil_water_per_minute_list[i]
                i += 1
            # Pumpe bereits eingeschaltet?
            if pump_deactivated():
                # Pumpe einschalten
                start_pump()
            # Pumpe ausgelastet oder keine Wassermenge > 0?
            # aendern!!!!
            # zu sprengende Zeit berechnen?
            pump_workload_temp = pump_workload()
            while pump_workload_temp + ventil_wateramount_list(get_highest_wateramount_ventil) <= get_pump_flow_capacity and ventil_wateramount_list(get_highest_wateramount_ventil) > 0:
                current_ventil_id = get_ventil_with_highest_time
                # starte bestimmtes Ventil
                start_ventil(current_ventil_id, ventil_time)
                # Setze Ventil-Zaehler zurueck
                ventil_wateramount_list[current_ventil_id] = 0
                pump_workload_temp = pump_workload_temp + ventil_wateramount_list(get_highest_wateramount_ventil)
    enable_automatic_irrigation = False


def time_allowed():
    date_today = date.today()
    # 0 - Montag bis 6-Sonntag
    day = date_today.weekday()
    # Sperrzeiten aus der Datenbank abrufen und pruefen, ob Sprengen aktuell erlaubt
    return True


def get_sensor_list():
    return Sensor.objects.all()


def get_valve_list():
    return Valve.objects.all()


def get_valve_sensor_list(sensor):
    return Valve.objects.filter(sensor_fk=sensor)


def set_water_amount_ventil(valve_id, watering_time):
    valves = Valve.objects.get(id=valve_id)
    valves.watering_time = watering_time
    valves.save()


def add_weathercounter_to_ventilcounter(valve_id, weather_counter):
    valves = Valve.objects.get(id=valve_id)
    valves.valve_counter = valves.valve_counter + weather_counter
    valves.save()


# Platzhalter fuer Pruefung, ob Sensor aktiv
def is_sensor_activ():
    return True


# Wassermenge berechnet fuer mit Sensor
def calculate_water_amount_sensor(sensor_id):
    wateramount = 0
    if is_rain_activ():
        rain_amount = get_rain_forecast() + get_rain_last_hour()
    else:
        rain_amount = 0
    if get_sensor_humidity(sensor_id) < get_sensor_threshold(sensor_id):
        # Wettereinfluesse die noch nicht vom Sensor erkannt wurden beruecksichtigen (Totzeit) und Forecast
        wateramount = calc_needed_water_amount() - get_sprinkler_last_hour() - rain_amount
        if wateramount < 0:
            wateramount = 0
    else:
        wateramount = 0
    return 10  # zum testen


def get_sensor_threshold(sensor_id):
    return Sensor.objects.get(id=sensor_id).moisture_threshold

def get_valve_threshold(valve_id):
    return Valve.objects.get(id=valve_id).valve_threshold

def calculate_water_amount_valve():
    return 1

# Abfrage an MC
def is_rain_activ():
    return True

#wo genau wird das gespeichert?
def get_rain_forecast():
    return 15

#Abfrage an MC
def get_sensor_humidity(sensor_id):
    return 10

#wahrscheinlich nicht mehr benoetigt
def get_rain_last_hour():
    return 0

# wahrscheinlich nicht mehr benoetigt
def get_sprinkler_last_hour():
    return 10

def calc_needed_water_amount():
    return 20

# Timons Spassgebiet

def get_pump_flow_capacity():
    return Pump.getObjects.First().flow_capacity  # evtl ID ergaenzen statt first

# SQL Statement fehlt noch
def get_highest_wateramount_ventil():
    # Absprache Dennis
    pass

# SQL Statement fehlt noch
def get_wateramount_valves():
    # Absprache mit Dennis
    pass

# SQL Statement fehlt noch
def get_ventils_water_per_minute(maria_db_connection):
    cursor = maria_db_connection.cursor()
    cursor.execute(
        "SELECT water_per_minute FROM ventil ORDER BY ID DESC"
    )
    results = cursor.fetchone()
    cursor.close()
    return results

# SQL Statement fehlt noch
def pump_deactivated(maria_db_connection):
    cursor = maria_db_connection.cursor()
    cursor.execute(
        # Wie kontrollieren wir die Aktivitaet der Pumpe?
        "SELECT activity FROM pump"
    )
    result = cursor.fetchone()[0]
    cursor.close()
    return result

# SQL Statement fehlt noch
def pump_workload(maria_db_connection):
    cursor = maria_db_connection.cursor()
    cursor.execute(
        # Wie kontrollieren wir die Aktivitaet der Pumpe?
        "SELECT workload FROM pump"
    )
    result = cursor.fetchone()
    cursor.close()
    return result

def get_ventil_with_highest_time():
    pass

    # Code unvollstaendig
def start_pump():
    pass
    # jo man keinen Plan davon!

# Code unvollstaendig
def shutdown_pump():
    pass
    # jo man keinen Plan davon!

# Code unvollstaendig
def start_ventil(ID):
    pass
    # jo man keinen Plan davon!

# Code unvollstaendig
def shutdown_ventil(ID):
    pass
