"""Support for Frequency Converter."""

from typing import List, Dict, Any, cast
import pandas as pd
from pygazpar.types.RelevesResultType import RelevesResultType
from pygazpar.enum import NatureReleve, QualificationReleve

# ------------------------------------------------------------------------------------------------------------
class FrequencyConverter:
    """Class for Convert daily data to other frequency."""
    INPUT_DATE_FORMAT = "%Y-%m-%d"
    OUTPUT_DATE_FORMAT = "%d/%m/%Y"
    OUTPUT2_DATE_FORMAT = "%Y-%m-%d "

    MONTHS = [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre"
    ]

    # ------------------------------------------------------
    @staticmethod
    def compute_hourly(daily: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compute hourly data."""

        return []

    # ------------------------------------------------------
    @staticmethod
    def compute_daily(daily: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Compute hourly data."""
        return daily

    # ------------------------------------------------------
    @staticmethod
    def compute_weekly(daily: List[RelevesResultType]) -> List[RelevesResultType]:
        """Compute Weekly data."""
        convertDaily = [ob.__dict__ for ob in daily]
        df = pd.DataFrame(convertDaily)

        # Trimming head and trailing spaces and convert to datetime.
        #df["date_time"] = pd.to_datetime(df["time_period"].str.strip(), format=FrequencyConverter.OUTPUT_DATE_FORMAT)
        df["journeeGaziere"] = pd.to_datetime(df["journeeGaziere"], format=FrequencyConverter.INPUT_DATE_FORMAT)

        # Get the first day of week.

        df["dateDebutReleve"] = pd.to_datetime(df["journeeGaziere"].dt.strftime("%W %Y 1T06:00:00"), format="%W %Y %wT%H:%M:%S")
        df["dateDebutReleve"]= df["dateDebutReleve"].dt.tz_localize("Europe/Paris")

        df["dateDebutWeek"] = pd.to_datetime(df["journeeGaziere"].dt.strftime("%W %Y 1"), format="%W %Y %w")
        # Get the last day of week.

        df["dateFinReleve"] = pd.to_datetime(df["journeeGaziere"].dt.strftime("%W %Y 0T06:00:00"), format="%W %Y %wT%H:%M:%S")
        df["dateFinReleve"]= df["dateFinReleve"].dt.tz_localize("Europe/Paris")
        df["dateFinReleve"]= df["dateFinReleve"]+pd.Timedelta(days=1)

        df["dateFinWeek"] = pd.to_datetime(df["journeeGaziere"].dt.strftime("%W %Y 0"), format="%W %Y %w")

        # Reformat the time period.
        df["time_period"] = "Du " + df["dateDebutWeek"].dt.strftime(FrequencyConverter.OUTPUT_DATE_FORMAT).astype(str) + " au " + df["dateFinWeek"].dt.strftime(FrequencyConverter.OUTPUT_DATE_FORMAT).astype(str)

        # Aggregate rows by month_year.
        df = df[["dateDebutReleve","dateFinReleve", "time_period", "indexDebut", "indexFin", "volumeBrutConsomme", "energieConsomme","temperature", "timestamp"]].groupby("time_period").agg(dateDebutReleve=('dateDebutReleve', 'min'),dateFinReleve=('dateFinReleve', 'max'), indexDebut=('indexDebut', 'min'), indexFin=('indexFin', 'max'), volumeBrutConsomme=('volumeBrutConsomme', 'sum'), energieConsomme=('energieConsomme', 'sum'),  temperature=('temperature', 'mean'),timestamp=('timestamp', 'min'), count=('energieConsomme', 'count')).reset_index()

        # Sort rows by month ascending.
        df = df.sort_values(by=['dateDebutReleve'])

        # Select rows where we have a full week (7 days) except for the current week.
        df = pd.concat([df[(df["count"] >= 7)], df.tail(1)[df.tail(1)["count"] < 7]])
        
        df['dateDebutReleve']=df['dateDebutReleve'].apply(FrequencyConverter.convert_datetime_iso_string)
        df['dateFinReleve']=df['dateFinReleve'].apply(FrequencyConverter.convert_datetime_iso_string)

        # Select target columns.
        df = df[["time_period","dateDebutReleve","dateFinReleve", "indexDebut", "indexFin", "volumeBrutConsomme", "energieConsomme","temperature", "timestamp"]]
        res = cast(List[Dict[str, Any]], df.to_dict('records'))
        result = [RelevesResultType(**dict(item, **{'natureReleve':NatureReleve.INFORMATIVES.value,'qualificationReleve':QualificationReleve.ESTIME.value})) for item in res]

        return result
    @staticmethod
    def convert_datetime_iso_string(x) -> str:
        """Compute Datetime to iso string data."""
        return pd.Timestamp(x).isoformat()
    # ------------------------------------------------------
    @staticmethod
    def compute_monthly(daily: List[RelevesResultType]) -> List[RelevesResultType]:
        """Compute Monthly data."""
        convertDaily = [ob.__dict__ for ob in daily]
        df = pd.DataFrame(convertDaily)

        # Trimming head and trailing spaces and convert to datetime.
        df["journeeGaziere"] = pd.to_datetime(df["journeeGaziere"], format=FrequencyConverter.INPUT_DATE_FORMAT)
        
        df["dateDebutReleve"] = pd.to_datetime(df["journeeGaziere"].dt.strftime("%Y %m 01T06:00:00"), format="%Y %m %dT%H:%M:%S")
        df["dateDebutReleve"]= df["dateDebutReleve"].dt.tz_localize("Europe/Paris")
        
        df["dateFinReleve"] = pd.to_datetime(df["journeeGaziere"].dt.strftime("%Y %m 01T06:00:00"), format="%Y %m %dT%H:%M:%S")
        df["dateFinReleve"]= df["dateFinReleve"].dt.tz_localize("Europe/Paris")
        df["dateFinReleve"]= df["dateFinReleve"]+pd.DateOffset(months=1)

        # Get the corresponding month-year.
        df["month_year"] = df["journeeGaziere"].apply(lambda x: FrequencyConverter.MONTHS[x.month - 1]).astype(str) + " " + df["journeeGaziere"].dt.strftime("%Y").astype(str)

        # Aggregate rows by month_year.
        #df = df[["date_time", "month_year", "start_index_m3", "end_index_m3", "volume_m3", "energy_kwh", "timestamp"]].groupby("month_year").agg(first_day_of_month=('date_time', 'min'), start_index_m3=('start_index_m3', 'min'), end_index_m3=('end_index_m3', 'max'), volume_m3=('volume_m3', 'sum'), energy_kwh=('energy_kwh', 'sum'), timestamp=('timestamp', 'min'), count=('energy_kwh', 'count')).reset_index()
        df = df[["dateDebutReleve","dateFinReleve", "month_year", "indexDebut", "indexFin", "volumeBrutConsomme", "energieConsomme","temperature", "timestamp"]].groupby("month_year").agg(dateDebutReleve=('dateDebutReleve', 'min'),dateFinReleve=('dateFinReleve', 'max'), indexDebut=('indexDebut', 'min'), indexFin=('indexFin', 'max'), volumeBrutConsomme=('volumeBrutConsomme', 'sum'), energieConsomme=('energieConsomme', 'sum'),  temperature=('temperature', 'mean'),timestamp=('timestamp', 'min'), count=('energieConsomme', 'count')).reset_index()

        # Sort rows by month ascending.
        df = df.sort_values(by=['dateDebutReleve'])

        # Select rows where we have a full month (more than 27 days) except for the current month.
        df = pd.concat([df[(df["count"] >= 28)], df.tail(1)[df.tail(1)["count"] < 28]])

        # Rename columns for their target names.
        df = df.rename(columns={"month_year": "time_period"})

        # Select target columns.
        df = df[["time_period","dateDebutReleve","dateFinReleve", "indexDebut", "indexFin", "volumeBrutConsomme", "energieConsomme","temperature", "timestamp"]]
        
        df['dateDebutReleve']=df['dateDebutReleve'].apply(FrequencyConverter.convert_datetime_iso_string)
        df['dateFinReleve']=df['dateFinReleve'].apply(FrequencyConverter.convert_datetime_iso_string)
        res = cast(List[Dict[str, Any]], df.to_dict('records'))
        result = [RelevesResultType(**dict(item, **{'natureReleve':NatureReleve.INFORMATIVES.value,'qualificationReleve':QualificationReleve.ESTIME.value})) for item in res]

        return result

    # ------------------------------------------------------
    @staticmethod
    def compute_yearly(daily: List[RelevesResultType]) -> List[RelevesResultType]:
        """Compute Yearly data."""
        convertDaily = [ob.__dict__ for ob in daily]
        df = pd.DataFrame(convertDaily)

        # Trimming head and trailing spaces and convert to datetime.
        df["journeeGaziere"] = pd.to_datetime(df["journeeGaziere"], format=FrequencyConverter.INPUT_DATE_FORMAT)

         
        df["dateDebutReleve"] = pd.to_datetime(df["journeeGaziere"].dt.strftime("%Y 01 01T06:00:00"), format="%Y %m %dT%H:%M:%S")
        df["dateDebutReleve"]= df["dateDebutReleve"].dt.tz_localize("Europe/Paris")
        
        df["dateFinReleve"] = pd.to_datetime(df["journeeGaziere"].dt.strftime("%Y 12 01T06:00:00"), format="%Y %m %dT%H:%M:%S")
        df["dateFinReleve"]= df["dateFinReleve"].dt.tz_localize("Europe/Paris")
        df["dateFinReleve"]= df["dateFinReleve"]+pd.DateOffset(months=1)
        # Get the corresponding year.
        df["year"] = df["journeeGaziere"].dt.strftime("%Y")

        # Aggregate rows by month_year.
        df = df[["year", "dateDebutReleve","dateFinReleve", "indexDebut", "indexFin","volumeBrutConsomme", "energieConsomme","temperature" "timestamp"]].groupby("year").agg(start_index_m3=('indexDebut', 'min'), end_index_m3=('indexFin', 'max'), volume_m3=('volumeBrutConsomme', 'sum'), energy_kwh=('energieConsomme', 'sum'),  temperature=('temperature', 'mean'),timestamp=('timestamp', 'min'), count=('energieConsomme', 'count')).reset_index()

        # Sort rows by month ascending.
        df = df.sort_values(by=['year'])

        # Select rows where we have almost a full year (more than 360) except for the current year.
        df = pd.concat([df[(df["count"] >= 360)], df.tail(1)[df.tail(1)["count"] < 360]])

        # Rename columns for their target names.
        df = df.rename(columns={"year": "time_period"})

        # Select target columns.
        df = df[["time_period",  "dateDebutReleve","dateFinReleve", "indexDebut", "indexFin","volumeBrutConsomme", "energieConsomme","temperature", "timestamp"]]
        
        df['dateDebutReleve']=df['dateDebutReleve'].apply(FrequencyConverter.convert_datetime_iso_string)
        df['dateFinReleve']=df['dateFinReleve'].apply(FrequencyConverter.convert_datetime_iso_string)
        res = cast(List[Dict[str, Any]], df.to_dict('records'))
        result = [RelevesResultType(**dict(item, **{'natureReleve':NatureReleve.INFORMATIVES.value,'qualificationReleve':QualificationReleve.ESTIME.value})) for item in res]

        return result
