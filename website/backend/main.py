from fastapi import FastAPI
from contextlib import asynccontextmanager
import tensorflow as tf
import joblib
from SequenceStandardScalerForBiLSTM import SequenceStandardScalerForBiLSTM
from collections import defaultdict
import sys
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Literal
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
import math
from calendar import isleap
from dateutil.relativedelta import relativedelta
from fastapi import Request
import re
import sqlite3
from fastapi.responses import FileResponse
from pathlib import Path

LANES_SEEDING_INSIDE_SWIM = (4, 5, 3, 6, 2, 7, 8, 1, 9, 0)

MIN_SWIMMER_DOB_DATE = date(1970, 1, 1)
MAX_SWIMMER_DOB_DATE = date(2050, 1, 1)
MIN_SWIMMER_HEIGHT = 70
MAX_SWIMMER_HEIGHT = 300
MIN_SWIM_DATETIME = datetime(2025, 1, 1)
MAX_SWIM_DATETIME = datetime(2050, 1, 1, 0, 0, 0, 0)
MIN_TIME_BETWEEN_PHASES = timedelta(minutes=15)  # Минимум 15 минут между фазами
DF_COLUMNS_LIST = [
    "race_number_in_phase",
    "races_in_phase",
    "swimmer_age_at_swim_start",
    "swimmer_id",
    "swimmer_lane",
    "swimmer_height",
    "is_swimmer_in_home_country",
    "swimmer_sex",
    "distance",
    "Backstroke",
    "Breaststroke",
    "Butterfly",
    "Freestyle",
    "Medley",
    "Africa",
    "Americas",
    "Asia",
    "Europe",
    "Oceania",
    "Finals",
    "Heats",
    "Semifinals",
    "pool_length",
    "has_race_date_local",
    "race_year",
    "race_month_sin",
    "race_month_cos",
    "race_doy_sin",
    "race_doy_cos",
    "race_dow_sin",
    "race_dow_cos",
    "has_race_time_local",
    "race_time_seconds_sin",
    "race_time_seconds_cos",
    "has_swimmer_dob",
    "swimmer_dob_year",
    "swimmer_dob_month_sin",
    "swimmer_dob_month_cos",
    "swimmer_dob_doy_sin",
    "swimmer_dob_doy_cos",
    "swimmer_dob_dow_sin",
    "swimmer_dob_dow_cos",
    "has_swimmer_lane",
    "has_swimmer_height",
    "swimmer_country_0",
    "swimmer_country_1",
    "swimmer_country_2",
    "swimmer_country_3",
    "swimmer_country_4",
    "swimmer_country_5",
    "swimmer_country_6",
    "swimmer_country_7",
    "host_country_0",
    "host_country_1",
    "host_country_2",
    "host_country_3",
    "host_country_4",
    "host_country_5",
    "host_country_6",
    "host_country_7",
    "swimmer_id_0",
    "swimmer_id_1",
    "swimmer_id_2",
    "swimmer_id_3",
    "swimmer_id_4",
    "swimmer_id_5",
    "swimmer_id_6",
    "swimmer_id_7",
    "swimmer_id_8",
    "swimmer_id_9",
    "swimmer_id_10",
    "swimmer_id_11",
    "swimmer_id_12",
    "swimmer_id_13",
    "swimmer_id_14",
    "swimmer_id_15",
]

sys.modules["__main__"].SequenceStandardScalerForBiLSTM = (
    SequenceStandardScalerForBiLSTM
)


# Препроцессор входных признаков специально для предсказания заплыва.
# Отличается от исходного препроцессора тем, что не использует входные записи в последовательностях
# Для других входных записе. То есть, все записи счиатются отдельно
class ColumnPreprocessorForSingleSwim:
    def __init__(self, original_preprocessor: SequenceStandardScalerForBiLSTM):
        self.original_preprocessor = original_preprocessor

    # Нам нужен только transform для прогноза, fit не нужен
    # (исходный препроцессор уже подогнан под трейн множество)
    def transform(self, X):
        # Отнормировать входные данные согласно обученному StandardScaler
        X_scaled = X.copy()
        feature_cols = self.original_preprocessor.feature_cols
        X_scaled[feature_cols] = self.original_preprocessor.scaler_.transform(
            X[feature_cols]
        )

        X_scaled["_original_idx"] = np.arange(len(X))

        # Выходной 3D массив на вход к модели
        sequences = np.zeros(
            (len(X), self.original_preprocessor.window_size, len(feature_cols)),
            dtype=np.float32,
        )
        for swimmer_id, group in X_scaled.groupby("swimmer_id", sort=False):
            # Пытаемся получить историю пловца
            history = self.original_preprocessor.swimmer_history.get(
                swimmer_id, np.zeros((0, len(feature_cols)), dtype=np.float32)
            )

            padding_size = max(  # Размер паддинга слева значениями -999
                0, self.original_preprocessor.window_size - 1 - len(history)
            )

            # Строим массив последовательностей
            prefix = None
            if padding_size > 0:
                paddings = np.full(
                    (padding_size, len(feature_cols)), -999.0, dtype=np.float32
                )  # (padding_size,n_features)
                prefix = np.vstack([paddings, history])  # (windows_size-1,n_features)
            else:
                prefix = np.vstack([history])  # (windows_size-1,n_features)
            cur_X_elems = group[feature_cols].values.astype(
                np.float32
            )  # (n_entries_for_swimmer, n_features)

            # Добавить ось в cur_X_elems
            cur_X_elems = cur_X_elems[
                :, np.newaxis, :
            ]  # (n_entries_for_swimmer,1,n_features)
            original_indices = group["_original_idx"].values

            # Скопировать prefix len(group) раз по первой оси 3D-массива
            prefix = np.tile(
                prefix, (len(group), 1, 1)
            )  # (n_entries_for_swimmer,window_size-1,n_features)

            # Объединить префиксы и текущие значения признаков в окна
            windows = np.concatenate(
                [prefix, cur_X_elems], axis=1
            )  # (n, window_size, n_features)

            # Записать признаки в выходной 3D массив
            sequences[original_indices] = windows

        return sequences


# Препроцессор входных признаков специально для предсказания фазы.
# Отличается от исходного препроцессора тем, что не использует входные записи в последовательностях
# Для других входных записе. То есть, все записи счиатются отдельно
class ColumnPreprocessorForSinglePhase:
    def __init__(self, original_preprocessor: SequenceStandardScalerForBiLSTM):
        self.original_preprocessor = original_preprocessor

    # Нам нужен только transform для прогноза, fit не нужен
    # (исходный препроцессор уже подогнан под трейн множество)
    # append_history - dict, где ключ - id пловца, а значение - np массив размерности (1 или 2,n_features)
    # (нужен для того, чтобы держать историю о предыдущих фазах дисциплины)
    def transform(self, X, append_history: dict):
        # Отнормировать входные данные согласно обученному StandardScaler
        X_scaled = X.copy()
        feature_cols = self.original_preprocessor.feature_cols
        X_scaled[feature_cols] = self.original_preprocessor.scaler_.transform(
            X[feature_cols]
        )

        X_scaled["_original_idx"] = np.arange(len(X))

        # Выходной 3D массив на вход к модели
        sequences = np.zeros(
            (len(X), self.original_preprocessor.window_size, len(feature_cols)),
            dtype=np.float32,
        )
        for swimmer_id, group in X_scaled.groupby("swimmer_id", sort=False):
            # Пытаемся получить историю пловца
            history = self.original_preprocessor.swimmer_history.get(
                swimmer_id, np.zeros((0, len(feature_cols)), dtype=np.float32)
            )

            if swimmer_id in append_history:
                history = history[len(append_history[swimmer_id]) :]

            padding_size = max(  # Размер паддинга слева значениями -999
                0,
                self.original_preprocessor.window_size
                - 1
                - len(history)
                - (
                    0
                    if swimmer_id not in append_history
                    else len(append_history[swimmer_id])
                ),
            )

            append_history_arr = append_history.get(
                swimmer_id, np.zeros((0, len(feature_cols)))
            )

            # Строим массив последовательностей
            prefix = None
            if padding_size > 0:
                paddings = np.full(
                    (padding_size, len(feature_cols)), -999.0, dtype=np.float32
                )  # (padding_size,n_features)
                prefix = np.vstack(
                    [paddings, history, append_history_arr]
                )  # (windows_size-1,n_features)
            else:
                prefix = np.vstack(
                    [history, append_history_arr]
                )  # (windows_size-1,n_features)
            cur_X_elems = group[feature_cols].values.astype(
                np.float32
            )  # (n_entries_for_swimmer, n_features)

            # Добавить ось в cur_X_elems
            cur_X_elems = cur_X_elems[
                :, np.newaxis, :
            ]  # (n_entries_for_swimmer,1,n_features)
            original_indices = group["_original_idx"].values

            # Скопировать prefix len(group) раз по первой оси 3D-массива
            prefix = np.tile(
                prefix, (len(group), 1, 1)
            )  # (n_entries_for_swimmer,window_size-1,n_features)

            # Объединить префиксы и текущие значения признаков в окна
            windows = np.concatenate(
                [prefix, cur_X_elems], axis=1
            )  # (n, window_size, n_features)

            # Записать признаки в выходной 3D массив
            sequences[original_indices] = windows

        return sequences


class SwimmerData(BaseModel):
    model_config = ConfigDict(
        extra="forbid", strict=True
    )  # Запретить дополнительные входные поля и приведение типов
    id: str
    full_name: str
    country_code: str | None = None
    height: float | None = Field(
        default=None, ge=MIN_SWIMMER_HEIGHT, le=MAX_SWIMMER_HEIGHT
    )  # Рост в см
    dob: date | None = Field(
        default=None,
        strict=False,
    )
    sex: Literal["M", "F"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    #
    # Выполняется при старте приложения
    #

    # Загрузить модели, препроцессор и преобразователь таргета
    app.state.model = tf.keras.models.load_model("BiLSTM_model.keras")
    # Преобразователь таргета который использовался при обучении
    app.state.features_preprocessor = joblib.load("features_preprocessor.joblib")
    # Преобразователь таргета для предсказания заплыва
    app.state.features_preprocessor_for_single_swim = ColumnPreprocessorForSingleSwim(
        app.state.features_preprocessor
    )
    # Преобразователь таргета для предсказания дисциплины
    app.state.features_preprocessor_for_single_discipline = (
        ColumnPreprocessorForSinglePhase(app.state.features_preprocessor)
    )
    app.state.target_transformer = joblib.load("target_transformer.joblib")

    # Загружаем словари (строка -> вектор эмбеддинга). И преобразовываем их в defaultdict
    tmp_dict_swimmer_id_embedds = joblib.load("swimmer_id_embedds.joblib")
    tmp_dict_swimmer_country_embedds = joblib.load("swimmer_country_embedds.joblib")
    tmp_dict_host_country_embedds = joblib.load("host_country_embedds.joblib")
    unk_swimmer_id_emb = tmp_dict_swimmer_id_embedds["[UNK]"]
    app.state.swimmer_id_embedds = defaultdict(
        lambda: unk_swimmer_id_emb, tmp_dict_swimmer_id_embedds
    )
    unk_swimmer_country_emb = tmp_dict_swimmer_country_embedds["[UNK]"]
    app.state.swimmer_country_embedds = defaultdict(
        lambda: unk_swimmer_country_emb,
        tmp_dict_swimmer_country_embedds,
    )
    unk_host_country_emb = tmp_dict_host_country_embedds["[UNK]"]
    app.state.host_country_embedds = defaultdict(
        lambda: unk_host_country_emb, tmp_dict_host_country_embedds
    )
    del tmp_dict_swimmer_id_embedds
    del tmp_dict_swimmer_country_embedds
    del tmp_dict_host_country_embedds

    app.state.male_swimmers_array = {}
    app.state.female_swimmers_array = {}
    app.state.male_swimmers_array_within_dob_limits = {}
    app.state.female_swimmers_array_within_dob_limits = {}
    with sqlite3.connect("swimmers_db.sqlite") as db:
        cursor = db.cursor()
        cursor.execute("SELECT id, full_name,dob,height,sex,country_code FROM swimmers")
        for row in cursor:
            newEntry = SwimmerData(
                id=row[0],
                full_name=row[1],
                dob=date.fromisoformat(row[2]) if row[2] else None,
                height=max(MIN_SWIMMER_HEIGHT, row[3]) if row[3] is not None else None,
                sex="F" if row[4] else "M",
                country_code=row[5],
            )
            if row[4] == 0:
                app.state.male_swimmers_array[row[0]] = newEntry
                if newEntry.dob is None or (
                    newEntry.dob < MAX_SWIMMER_DOB_DATE
                    and newEntry.dob >= MIN_SWIMMER_DOB_DATE
                ):
                    app.state.male_swimmers_array_within_dob_limits[row[0]] = newEntry
            else:
                app.state.female_swimmers_array[row[0]] = newEntry
                if newEntry.dob is None or (
                    newEntry.dob < MAX_SWIMMER_DOB_DATE
                    and newEntry.dob >= MIN_SWIMMER_DOB_DATE
                ):
                    app.state.female_swimmers_array_within_dob_limits[row[0]] = newEntry

    yield
    #
    # Выполняется при остановке приложения
    #


app = FastAPI(
    title="Swimming prediction service API",
    version="1.0.0",
    description="Сервис для прогноза результатов по плаванию",
    lifespan=lifespan,
)


class SwimmerRaceEntry(BaseModel):
    model_config = ConfigDict(
        extra="forbid", strict=True
    )  # Запретить дополнительные входные поля и приведение типов
    lane: int = Field(ge=0, le=9)
    id: str
    country_code: str | None = None
    height: float | None = Field(
        default=None, ge=MIN_SWIMMER_HEIGHT, le=MAX_SWIMMER_HEIGHT
    )  # Рост в см
    dob: date | None = Field(
        default=None, strict=False, ge=MIN_SWIMMER_DOB_DATE, lt=MAX_SWIMMER_DOB_DATE
    )

    # Проверить, что дата в нужном формате
    @field_validator("dob", mode="before")
    def validate_dob(cls, val):
        if isinstance(val, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", val):
                raise ValueError("Error: swimmer dob must be in format YYYY-MM-DD")
        return val  # Если не строка - отправляем на дальнейшую проверку


class Point(BaseModel):
    x: float
    y: float
    is_current_dot: Literal[
        0, 1
    ]  # Является ли точка действительным значением а не просто сценарием


class SwimmerRaceEntryWithResults(SwimmerRaceEntry):
    predicted_time: float
    predicted_place_in_swim: int
    graph_age_dependency: list[Point] | None
    graph_height_dependency: list[Point] | None
    graph_lane_dependency: list[Point]


class SwimEntryForSwim(BaseModel):
    model_config = ConfigDict(
        extra="forbid", strict=True
    )  # Запретить дополнительные входные поля и приведение типов

    swim_sex: Literal["M", "F"]
    swim_distance: Literal[50, 100, 200, 400, 800, 1500]  # Дистанция заплыва в метрах
    swim_style: Literal[
        "Freestyle", "Butterfly", "Backstroke", "Breaststroke", "Medley"
    ]
    swim_pool_length: Literal[25, 50]  # Длина бассейна в метрах
    swim_phase: Literal["Semifinals", "Heats", "Finals"]
    swim_datetime_local_iso: datetime = Field(
        strict=False, ge=MIN_SWIM_DATETIME, lt=MAX_SWIM_DATETIME
    )
    host_country_code: str
    host_region: Literal["Oceania", "Africa", "Americas", "Europe", "Asia"]
    swimmers_array: list[SwimmerRaceEntry] = Field(min_length=1, max_length=10)

    # Проверить, что дата и время в нужном формате
    @field_validator("swim_datetime_local_iso", mode="before")
    def validate_swim_datetime(cls, val):
        if isinstance(val, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", val):
                raise ValueError(
                    "Error: swim_datetime must be in format YYYY-MM-DDTHH:MM:SS"
                )
        return val  # Если не строка - отправляем на дальнейшую проверку

    # Дополнительная валидация после проверки типов полей
    @model_validator(mode="after")
    def validate_unique_swimmer_lanes(self):
        lanes = [swimmer.lane for swimmer in self.swimmers_array]
        if len(lanes) != len(set(lanes)):
            raise ValueError("Error: lane number must be unique within race")
        return self

    @model_validator(mode="after")
    def validate_unique_swimmer_ids(self):
        ids = [swimmer.id for swimmer in self.swimmers_array]
        if len(ids) != len(set(ids)):
            raise ValueError("Error: swimmer_id must be unique within race")
        return self

    @model_validator(mode="after")
    def validate_swimmer_age(self):
        swim_date = self.swim_datetime_local_iso.date()
        for swimmer in self.swimmers_array:
            if type(swimmer.dob) == date:
                if swim_date < swimmer.dob:
                    raise ValueError(
                        f"Swimmer {swimmer.id} date of birth is after the race date!"
                    )

                # Проверка на то что пловец не слишком стар и не слишком молод на момент старта заплыва
                age = relativedelta(swim_date, swimmer.dob).years  # Возраст пловца

                if age < 12:
                    raise ValueError(
                        f"Swimmer {swimmer.id} is too young (age {age}, minimum age for prediction is 12)!"
                    )
                elif age > 120:
                    raise ValueError(
                        f"Swimmer {swimmer.id} is too old (age {age}, maximum age for prediction is 120)!"
                    )
        return self

    @model_validator(mode="after")
    def validate_swimmer_sex(
        self,
    ):  # Проверить что пол пловцов совпадает с полом заплыва
        swim_sex: str = self.swim_sex
        for swimmer in self.swimmers_array:
            found_in_male_dict = swimmer.id in app.state.male_swimmers_array
            found_in_female_dict = swimmer.id in app.state.female_swimmers_array
            if (
                swim_sex == "F"
                and found_in_male_dict
                or swim_sex == "M"
                and found_in_female_dict
            ):
                raise ValueError(
                    f"Swimmer {swimmer.id} is of wrong sex (only {'male' if swim_sex=='M' else 'female'} are allowed in this swim)!"
                )
        return self


class SwimEntryForSwimWithResults(SwimEntryForSwim):
    swimmers_array: list[SwimmerRaceEntryWithResults]


def calculate_swimmer_age_at_swim_start(
    swimmer_dob: date | None, swim_datetime: datetime
):
    if swimmer_dob is None:
        return 20  # Медиана возрастов пловцов
    return (swim_datetime.date() - swimmer_dob).days // 365


def calculate_swimmer_height(swimmer_height: float | None):
    if swimmer_height is None:
        return 180  # Медиана роста пловцов
    return swimmer_height


def calculate_is_swimmer_in_home_country(
    swimmer_country_code: str | None, host_country_code: str
):
    if swimmer_country_code is None or swimmer_country_code != host_country_code:
        return 0
    return 1


def calculate_swimmer_sex(swimmer_sex: str):
    if swimmer_sex == "M":
        return 0
    return 1


def get_swim_doy_sin_cos(swim_date: datetime):
    timetuple = swim_date.timetuple()
    doy = timetuple.tm_yday
    days_in_year = 366 if isleap(swim_date.year) else 365
    return (
        math.sin(2 * math.pi * doy / days_in_year),
        math.cos(2 * math.pi * doy / days_in_year),
    )


def get_swim_seconds_in_day_sin_cos(swim_date: datetime):
    seconds_in_day = swim_date.second + swim_date.minute * 60 + swim_date.hour * 60 * 60
    return (
        math.sin(2 * math.pi * seconds_in_day / (60 * 60 * 24)),
        math.cos(2 * math.pi * seconds_in_day / (60 * 60 * 24)),
    )


def calculate_swimmer_dob_year_monthsin_monthcos_doysin_doycos_dowsin_dowcos(
    swim_dt: datetime, swimmer_dob: date | None
):
    if (
        swimmer_dob is None
    ):  # Считаем что возраст пловца = 20 (медиана) и вычитаем из текущей даты 20 лет
        swimmer_dob = (swim_dt - relativedelta(years=20)).date()
    year = swimmer_dob.year
    month_angle = 2 * math.pi * swimmer_dob.month / 12
    monthsin = math.sin(month_angle)
    monthcos = math.cos(month_angle)
    doy_angle = (
        2
        * math.pi
        * swimmer_dob.timetuple().tm_yday
        / (366 if isleap(swimmer_dob.year) else 365)
    )
    doysin = math.sin(doy_angle)
    doycos = math.cos(doy_angle)
    dow_angle = 2 * math.pi * swimmer_dob.weekday() / 7
    dowsin = math.sin(dow_angle)
    dowcos = math.cos(dow_angle)
    return (year, monthsin, monthcos, doysin, doycos, dowsin, dowcos)


# Создать записи для одного пловца
def create_entries_for_single_swimmer_for_swim_prediction(
    swim_data: SwimEntryForSwim, swimmer: SwimmerRaceEntry, request: Request
) -> tuple[list[dict], list[int] | None, list[date] | None, list[int], list[int]]:
    # Вернуть колонки и значения аргументов для графиков: сначала массив для роста,
    # потом для возраста, затем для дорожки. Далее массив с индексом текущего
    # элемента в рамках предсказания
    cur_swimmer_dob = swimmer.dob
    cur_swimmer_height = swimmer.height
    cur_swimmer_lane = swimmer.lane
    rows = []
    cur_element_indices_in_predictions = []
    # Сначала записываем оригинальное предсказание
    row = {
        "race_number_in_phase": 1,
        "races_in_phase": 1,
        "swimmer_age_at_swim_start": (
            calculate_swimmer_age_at_swim_start(
                swimmer.dob, swim_data.swim_datetime_local_iso
            )
        ),
        "swimmer_id": swimmer.id,
        "swimmer_lane": swimmer.lane,
        "swimmer_height": calculate_swimmer_height(swimmer.height),
        "is_swimmer_in_home_country": calculate_is_swimmer_in_home_country(
            swimmer.country_code, swim_data.host_country_code
        ),
        "swimmer_sex": calculate_swimmer_sex(swim_data.swim_sex),
        "distance": swim_data.swim_distance,
        "Backstroke": 1 if swim_data.swim_style == "Backstroke" else 0,
        "Breaststroke": 1 if swim_data.swim_style == "Breaststroke" else 0,
        "Butterfly": 1 if swim_data.swim_style == "Butterfly" else 0,
        "Freestyle": 1 if swim_data.swim_style == "Freestyle" else 0,
        "Medley": 1 if swim_data.swim_style == "Medley" else 0,
        "Africa": 1 if swim_data.host_region == "Africa" else 0,
        "Americas": 1 if swim_data.host_region == "Americas" else 0,
        "Asia": 1 if swim_data.host_region == "Asia" else 0,
        "Europe": 1 if swim_data.host_region == "Europe" else 0,
        "Oceania": 1 if swim_data.host_region == "Oceania" else 0,
        "Finals": 1 if swim_data.swim_phase == "Finals" else 0,
        "Heats": 1 if swim_data.swim_phase == "Heats" else 0,
        "Semifinals": 1 if swim_data.swim_phase == "Semifinals" else 0,
        "pool_length": swim_data.swim_pool_length,
        "has_race_date_local": 1,
        "race_year": swim_data.swim_datetime_local_iso.year,
        "race_month_sin": math.sin(
            2 * math.pi * swim_data.swim_datetime_local_iso.month / 12
        ),
        "race_month_cos": math.cos(
            2 * math.pi * swim_data.swim_datetime_local_iso.month / 12
        ),
        "race_doy_sin": (
            doy_sin_cos := get_swim_doy_sin_cos(swim_data.swim_datetime_local_iso)
        )[0],
        "race_doy_cos": doy_sin_cos[1],
        "race_dow_sin": math.sin(
            2 * math.pi * swim_data.swim_datetime_local_iso.weekday() / 7
        ),
        "race_dow_cos": math.cos(
            2 * math.pi * swim_data.swim_datetime_local_iso.weekday() / 7
        ),
        "has_race_time_local": 1,
        "race_time_seconds_sin": (
            seconds_of_day := get_swim_seconds_in_day_sin_cos(
                swim_data.swim_datetime_local_iso
            )
        )[0],
        "race_time_seconds_cos": seconds_of_day[1],
        "has_swimmer_dob": 0 if swimmer.dob is None else 1,
        "swimmer_dob_year": (
            dob_data := calculate_swimmer_dob_year_monthsin_monthcos_doysin_doycos_dowsin_dowcos(
                swim_data.swim_datetime_local_iso, swimmer.dob
            )
        )[0],
        "swimmer_dob_month_sin": dob_data[1],
        "swimmer_dob_month_cos": dob_data[2],
        "swimmer_dob_doy_sin": dob_data[3],
        "swimmer_dob_doy_cos": dob_data[4],
        "swimmer_dob_dow_sin": dob_data[5],
        "swimmer_dob_dow_cos": dob_data[6],
        "has_swimmer_lane": 1,
        "has_swimmer_height": 0 if swimmer.height is None else 1,
    }
    swimmer_country_embedding = request.app.state.swimmer_country_embedds[
        swimmer.country_code
    ]
    host_country_embedding = request.app.state.host_country_embedds[
        swim_data.host_country_code
    ]
    swimmer_id_embedding = request.app.state.swimmer_id_embedds[swimmer.id]
    for i in range(8):
        row[f"swimmer_country_{i}"] = swimmer_country_embedding[i]
    for i in range(8):
        row[f"host_country_{i}"] = host_country_embedding[i]
    for i in range(16):
        row[f"swimmer_id_{i}"] = swimmer_id_embedding[i]
    rows.append(row)

    heights = []
    ages = []
    lanes = []
    # Теперь записиваем входы для создания предсказаний для графика "зависимость от роста"
    if cur_swimmer_height is not None:
        # От -5 см до +5 см
        indice = -1
        for height_delta in range(-5, 6, 1):
            indice += 1
            rows.append(row.copy())
            rows[-1]["swimmer_height"] = cur_swimmer_height + height_delta
            heights.append(cur_swimmer_height + height_delta)
            if height_delta == 0:
                cur_element_indices_in_predictions.append(indice)
    else:
        heights = None
        cur_element_indices_in_predictions.append(None)

    # Теперь записиваем входы для создания предсказаний для графика "зависимость от возраста"
    if cur_swimmer_dob is not None:
        # От -5 лет до +5 лет
        indice = -1
        for age_delta in range(-5, 6, 1):
            indice += 1
            rows.append(row.copy())
            dob_data = calculate_swimmer_dob_year_monthsin_monthcos_doysin_doycos_dowsin_dowcos(
                swim_data.swim_datetime_local_iso,
                cur_swimmer_dob - relativedelta(years=age_delta),
            )
            rows[-1]["swimmer_age_at_swim_start"] = (
                rows[0]["swimmer_age_at_swim_start"] + age_delta
            )
            rows[-1]["swimmer_dob_year"] = dob_data[0]
            rows[-1]["swimmer_dob_month_sin"] = dob_data[1]
            rows[-1]["swimmer_dob_month_cos"] = dob_data[2]
            rows[-1]["swimmer_dob_doy_sin"] = dob_data[3]
            rows[-1]["swimmer_dob_doy_cos"] = dob_data[4]
            rows[-1]["swimmer_dob_dow_sin"] = dob_data[5]
            rows[-1]["swimmer_dob_dow_cos"] = dob_data[6]
            ages.append(rows[-1]["swimmer_age_at_swim_start"])
            if age_delta == 0:
                cur_element_indices_in_predictions.append(indice)
    else:
        ages = None
        cur_element_indices_in_predictions.append(None)

    # Теперь записиваем входы для создания предсказаний для графика "зависимость от номера дорожки"
    for lane in range(0, 10, 1):
        rows.append(row.copy())
        rows[-1]["swimmer_lane"] = lane
        lanes.append(lane)
        if lane == cur_swimmer_lane:
            cur_element_indices_in_predictions.append(lane)

    return (
        rows,
        heights,
        ages,
        lanes,
        cur_element_indices_in_predictions,
    )


# Получить предсказание заплыва
@app.post("/swimPrediction")
def swimPrediction(
    swim_data: SwimEntryForSwim, request: Request
) -> SwimEntryForSwimWithResults:
    # Составляем датафрейм
    rows = []
    heights_for_graph_dict: dict[str, list[float]] = {}
    ages_for_graph_dict: dict[str, list[int]] = {}
    lanes_for_graph_dict: dict[str, list[int]] = {}
    indices_for_graphs_dict: dict[str, list[int]] = {}
    for swimmer_arr_elem in swim_data.swimmers_array:
        entry_data = create_entries_for_single_swimmer_for_swim_prediction(
            swim_data, swimmer_arr_elem, request
        )
        rows.extend(entry_data[0])
        heights_for_graph_dict[swimmer_arr_elem.id] = entry_data[1]
        ages_for_graph_dict[swimmer_arr_elem.id] = entry_data[2]
        lanes_for_graph_dict[swimmer_arr_elem.id] = entry_data[3]
        indices_for_graphs_dict[swimmer_arr_elem.id] = entry_data[4]

    df = pd.DataFrame(rows, columns=DF_COLUMNS_LIST)

    # Получение предсказаний
    predictions = request.app.state.model.predict(
        request.app.state.features_preprocessor_for_single_swim.transform(df)
    )
    # Инверсия масштабирования признаков
    predictions = request.app.state.target_transformer.inverse_transform(
        predictions.reshape(-1, 1)
    ).ravel()

    # Формирование ответа
    predicted_times = []
    for ind in range(len(predictions)):
        # Если поменялся id пловца - значит эта запись - предсказание на введенных пользователем данных, а не для графиков
        swimmer_id = df.iloc[ind]["swimmer_id"]
        if ind == 0 or df.iloc[ind - 1]["swimmer_id"] != swimmer_id:
            predicted_times.append(
                {
                    "swimmer_id": df.iloc[ind]["swimmer_id"],
                    "predicted_time": float(max(10, predictions[ind])),
                }
            )
    predicted_times = sorted(predicted_times, key=lambda x: x["predicted_time"])
    from_swimmer_id_to_place = {
        elem["swimmer_id"]: i + 1 for i, elem in enumerate(predicted_times)
    }
    swimmers_array = []
    cur_ind = 0
    for swimmer in swim_data.swimmers_array:
        predicted_time = float(max(10, predictions[cur_ind]))
        cur_ind += 1
        graph_age_dependency: list[Point] | None = []
        graph_height_dependency: list[Point] | None = []
        graph_lane_dependency: list[Point] = []

        # Формируем массив для графика зависимости от роста
        if heights_for_graph_dict[swimmer.id] is None:
            graph_height_dependency = None
        else:
            for i, height in enumerate(heights_for_graph_dict[swimmer.id]):
                point_x = height
                point_y = float(max(10, predictions[cur_ind]))
                point_is_current_dot = (
                    1 if i == indices_for_graphs_dict[swimmer.id][0] else 0
                )
                cur_ind += 1
                graph_height_dependency.append(
                    Point(x=point_x, y=point_y, is_current_dot=point_is_current_dot)
                )

        # Формируем массив для графика зависимости от возраста
        if ages_for_graph_dict[swimmer.id] is None:
            graph_age_dependency = None
        else:
            for i, age in enumerate(ages_for_graph_dict[swimmer.id]):
                point_x = age
                point_y = float(max(10, predictions[cur_ind]))
                point_is_current_dot = (
                    1 if i == indices_for_graphs_dict[swimmer.id][1] else 0
                )
                cur_ind += 1
                graph_age_dependency.append(
                    Point(x=point_x, y=point_y, is_current_dot=point_is_current_dot)
                )

        # Формируем массив для графика зависимости от дорожки
        for i, lane in enumerate(lanes_for_graph_dict[swimmer.id]):
            point_x = lane
            point_y = float(max(10, predictions[cur_ind]))
            point_is_current_dot = (
                1 if i == indices_for_graphs_dict[swimmer.id][2] else 0
            )
            cur_ind += 1
            graph_lane_dependency.append(
                Point(x=point_x, y=point_y, is_current_dot=point_is_current_dot)
            )

        swimmers_array.append(
            SwimmerRaceEntryWithResults(
                **swimmer.model_dump(),
                predicted_time=predicted_time,
                graph_age_dependency=graph_age_dependency,
                graph_height_dependency=graph_height_dependency,
                graph_lane_dependency=graph_lane_dependency,
                predicted_place_in_swim=from_swimmer_id_to_place[swimmer.id],
            )
        )
    results: SwimEntryForSwimWithResults = SwimEntryForSwimWithResults(
        **swim_data.model_dump(exclude={"swimmers_array"}),
        swimmers_array=swimmers_array,
    )

    return results


# Получить словарь пловцов (ключ - id пловца)
@app.get("/swimmersDict/{swimmers_sex}")
def get_swimmers_dict(swimmers_sex: Literal["M", "F"]) -> dict[str, SwimmerData]:
    if swimmers_sex == "M":
        return app.state.male_swimmers_array_within_dob_limits
    else:
        return app.state.female_swimmers_array_within_dob_limits


@app.get("/")
def getMainPage():
    html_path = Path(__file__).parent.parent / "frontend" / "index.html"
    return FileResponse(html_path)


@app.get("/swim")
def getSwimPage():
    html_path = Path(__file__).parent.parent / "frontend" / "swim.html"
    return FileResponse(html_path)


@app.get("/discipline")
def getDisciplinePage():
    html_path = Path(__file__).parent.parent / "frontend" / "discipline.html"
    return FileResponse(html_path)


class SwimEntryForDisciplineWithoutSwimmers(BaseModel):
    model_config = ConfigDict(
        extra="forbid", strict=True
    )  # Запретить дополнительные входные поля и приведение типов

    swim_datetime_local_iso: datetime = Field(
        strict=False, ge=MIN_SWIM_DATETIME, lt=MAX_SWIM_DATETIME
    )

    # Проверить, что дата и время в нужном формате
    @field_validator("swim_datetime_local_iso", mode="before")
    def validate_swim_datetime(cls, val):
        if isinstance(val, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", val):
                raise ValueError(
                    "Error: swim_datetime must be in format YYYY-MM-DDTHH:MM:SS"
                )
        return val  # Если не строка - отправляем на дальнейшую проверку


class SwimEntryForDisciplineWithSwimmers(BaseModel):
    model_config = ConfigDict(
        extra="forbid", strict=True
    )  # Запретить дополнительные входные поля и приведение типов

    swim_datetime_local_iso: datetime = Field(
        strict=False, ge=MIN_SWIM_DATETIME, lt=MAX_SWIM_DATETIME
    )
    swimmers_array: list[SwimmerRaceEntry] = Field(min_length=1, max_length=10)

    # Проверить, что дата и время в нужном формате
    @field_validator("swim_datetime_local_iso", mode="before")
    def validate_swim_datetime(cls, val):
        if isinstance(val, str):
            if not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", val):
                raise ValueError(
                    "Error: swim_datetime must be in format YYYY-MM-DDTHH:MM:SS"
                )
        return val  # Если не строка - отправляем на дальнейшую проверку

    # Дополнительная валидация после проверки типов полей
    @model_validator(mode="after")
    def validate_unique_swimmer_lanes(self):
        lanes = [swimmer.lane for swimmer in self.swimmers_array]
        if len(lanes) != len(set(lanes)):
            raise ValueError("Error: lane number must be unique within race")
        return self

    @model_validator(mode="after")
    def validate_swimmer_age(self):
        swim_date = self.swim_datetime_local_iso.date()
        for swimmer in self.swimmers_array:
            if type(swimmer.dob) == date:
                if swim_date < swimmer.dob:
                    raise ValueError(
                        f"Swimmer {swimmer.id} date of birth is after the race date!"
                    )

                # Проверка на то что пловец не слишком стар и не слишком молод на момент старта заплыва
                age = relativedelta(swim_date, swimmer.dob).years  # Возраст пловца

                if age < 12:
                    raise ValueError(
                        f"Swimmer {swimmer.id} is too young (age {age}, minimum age for prediction is 12)!"
                    )
                elif age > 120:
                    raise ValueError(
                        f"Swimmer {swimmer.id} is too old (age {age}, maximum age for prediction is 120)!"
                    )
        return self

class SwimmerRaceEntryWithResultsForDiscipline(SwimmerRaceEntryWithResults):
    predicted_place_in_phase:int=Field(ge=1)
    


class SwimEntryForDisciplineWithSwimmersWithResults(SwimEntryForDisciplineWithSwimmers):
    swimmers_array: list[SwimmerRaceEntryWithResultsForDiscipline] = Field(
        min_length=1, max_length=10
    )


# Класс для дисциплины
class DisciplineEntry(BaseModel):
    model_config = ConfigDict(
        extra="forbid", strict=True
    )  # Запретить дополнительные входные поля и приведение типов

    discipline_sex: Literal["M", "F"]
    discipline_distance: Literal[
        50, 100, 200, 400, 800, 1500
    ]  # Дистанция дистанции в метрах
    discipline_style: Literal[
        "Freestyle", "Butterfly", "Backstroke", "Breaststroke", "Medley"
    ]
    discipline_pool_length: Literal[25, 50]  # Длина бассейна в метрах
    host_country_code: str
    host_region: Literal["Oceania", "Africa", "Americas", "Europe", "Asia"]

    heats_phase_swims: list[SwimEntryForDisciplineWithSwimmers] | None = Field( 
        default=None, min_length=2, max_length=30
    )  # От 2 до 30 отборочных заплывов
    finals_phase_swims: ( 
        list[SwimEntryForDisciplineWithSwimmers]
        | list[SwimEntryForDisciplineWithoutSwimmers]
    ) = Field( 
        min_length=1, max_length=30
    )  # От 1 до 30 финалов
    semifinals_phase_swims: (
        list[SwimEntryForDisciplineWithSwimmers]
        | list[SwimEntryForDisciplineWithoutSwimmers]
        | None
    ) = Field( default=None,
        min_length=2, max_length=2
    )  # Всегда 2 полуфинала

    # Проверить что самая ранняя фаза имеет пловцов в себе, а самая поздняя - не имеет.
    @model_validator(mode="after")
    def validate_swim_phases(self):
        # Если финалы прямые (>1 финала), то проверяем, что остальные фазы - None и что в финалах содержатся пловцы
        if len(self.finals_phase_swims) > 1:
            if self.heats_phase_swims is not None:
                raise ValueError(
                    "Error: heats_phase_swims must be null when direct finals are anticipated (more than 1 finals swims)"
                )
            if self.semifinals_phase_swims is not None:
                raise ValueError(
                    "Error: semifinals_phase_swims must be null when direct finals are anticipated (more than 1 finals swims)"
                )
            if (
                type(self.finals_phase_swims[0])
                is SwimEntryForDisciplineWithoutSwimmers
            ):
                raise ValueError(
                    "Error: swimmers data should be entered in finals when direct finals are anticipated (more than 1 finals swims)"
                )
            return self
        #Если же финал ровно 1, то он будет прямым только если остальные фазы - None
        if len(self.finals_phase_swims)==1 and self.semifinals_phase_swims is None and self.heats_phase_swims is None:
            #Проверим, что финальный заплыв содержит пловцов
            if (
                type(self.finals_phase_swims[0])
                is SwimEntryForDisciplineWithoutSwimmers
            ):
                raise ValueError(
                    "Error: swimmers data should be entered in finals when direct finals are anticipated (1 finals swims and no other swims)"
                )
            return self
        # Если финалы непрямые, то проверяем, что в финалах нет пловцов
        if type(self.finals_phase_swims[0]) is SwimEntryForDisciplineWithSwimmers:
            raise ValueError(
                "Error: swimmers data should not be entered in finals when direct finals are not anticipated (exactly 1 finals swim)"
            )
        # Если есть фаза полуфиналов и финалы непрямые, то проверяем, что фазы heats не существует и в фазе полуфиналов есть пловцы, либо фаза heats существует и в фазе полуфиналов нет пловцов.
        if self.semifinals_phase_swims is not None:
            if (
                type(self.semifinals_phase_swims[0])
                is SwimEntryForDisciplineWithSwimmers
            ):
                if self.heats_phase_swims is not None:
                    raise ValueError(
                        "Error: heats_phase_swims should be null when semifinals is expected to be the first phase of the discipline (when it has swimmers data in it)"
                    )
            if (
                type(self.semifinals_phase_swims[0])
                is SwimEntryForDisciplineWithoutSwimmers
            ):
                if self.heats_phase_swims is None:
                    raise ValueError(
                        "Error: heats_phase_swims should not be null when semifinals is expected to be the second phase of the discipline (when it has not swimmers data in it)"
                    )
            return self
        # Если фазы полуфиналов нет и финалы непрямые, то проверяем, что фаза heats существует
        if self.semifinals_phase_swims is None:
            if self.heats_phase_swims is None:
                raise ValueError(
                    "Error: heats_phase_swims should not be null when finals is expected to be the second phase of the discipline (when it has not swimmers data in it)"
                )

        return self

    # Проверить, что пловцы во всех заплывах начальной фазы уникальны
    @model_validator(mode="after")
    def validate_unique_swimmer_ids(self):
        ids = None
        if self.heats_phase_swims is not None:
            ids = [
                swimmer.id
                for swim in self.heats_phase_swims
                for swimmer in swim.swimmers_array
            ]
        elif self.semifinals_phase_swims is not None:
            ids = [
                swimmer.id
                for swim in self.semifinals_phase_swims
                for swimmer in swim.swimmers_array
            ]
        else:
            ids = [
                swimmer.id
                for swim in self.finals_phase_swims
                for swimmer in swim.swimmers_array
            ]
        if len(ids) != len(set(ids)):
            raise ValueError(
                "Error: swimmer_id must be unique within first phase of discipline"
            )
        return self

    @model_validator(mode="after")
    def validate_swimmer_sex(
        self,
    ):  # Проверить что пол пловцов совпадает с полом дисциплины
        discipline_sex: str = self.discipline_sex
        swimmers_ids = None
        if self.heats_phase_swims is not None:
            swimmers_ids = [
                swimmer.id
                for swim in self.heats_phase_swims
                for swimmer in swim.swimmers_array
            ]
        elif self.semifinals_phase_swims is not None:
            swimmers_ids = [
                swimmer.id
                for swim in self.semifinals_phase_swims
                for swimmer in swim.swimmers_array
            ]
        else:
            swimmers_ids = [
                swimmer.id
                for swim in self.finals_phase_swims
                for swimmer in swim.swimmers_array
            ]
        for swimmer_id in swimmers_ids:
            found_in_male_dict = swimmer_id in app.state.male_swimmers_array
            found_in_female_dict = swimmer_id in app.state.female_swimmers_array
            if (
                discipline_sex == "F"
                and found_in_male_dict
                or discipline_sex == "M"
                and found_in_female_dict
            ):
                raise ValueError(
                    f"Swimmer {swimmer_id} is of wrong sex (only {'male' if discipline_sex=='M' else 'female'} are allowed in this swim)!"
                )
        return self

    # Проверить что фазы идут по порядку (heats -> semifinals -> finals), и что заплывы в рамках фазы отсортированы по времени начала.
    # Минимальное время между фазами возьмём из константы
    @model_validator(mode="after")
    def validate_swims_time_order(self):
        if self.heats_phase_swims is not None:
            for i in range(1, len(self.heats_phase_swims)):
                if (
                    self.heats_phase_swims[i].swim_datetime_local_iso
                    < self.heats_phase_swims[i - 1].swim_datetime_local_iso
                ):
                    raise ValueError(
                        "Error: swims inside heats phase should be sorted by start datetime!"
                    )
        if self.finals_phase_swims is not None:
            for i in range(1, len(self.finals_phase_swims)):
                if (
                    self.finals_phase_swims[i].swim_datetime_local_iso
                    < self.finals_phase_swims[i - 1].swim_datetime_local_iso
                ):
                    raise ValueError(
                        "Error: swims inside finals phase should be sorted by start datetime!"
                    )
        if self.semifinals_phase_swims is not None:
            for i in range(1, len(self.semifinals_phase_swims)):
                if (
                    self.semifinals_phase_swims[i].swim_datetime_local_iso
                    < self.semifinals_phase_swims[i - 1].swim_datetime_local_iso
                ):
                    raise ValueError(
                        "Error: swims inside semifinals phase should be sorted by start datetime!"
                    )
        # Если фаза полуфинала существует, то между началом последнего заплыва полуфинала и началом первого заплыва финала должна быть разница во времени
        if self.semifinals_phase_swims is not None:
            if (
                self.semifinals_phase_swims[-1].swim_datetime_local_iso
                + MIN_TIME_BETWEEN_PHASES
                > self.finals_phase_swims[0].swim_datetime_local_iso
            ):
                raise ValueError(
                    f"Error: difference between last semifinals swim and the final swim should be not less than {MIN_TIME_BETWEEN_PHASES}!"
                )
        # Иначе, если фаза отборочных существует, то между началом последнего заплыва отборочных и началом первого заплыва финала должна быть разница во времени
        elif self.heats_phase_swims is not None:
            if (
                self.heats_phase_swims[-1].swim_datetime_local_iso
                + MIN_TIME_BETWEEN_PHASES
                > self.finals_phase_swims[0].swim_datetime_local_iso
            ):
                raise ValueError(
                    f"Error: difference between last heats swim and the final swim should be not less than {MIN_TIME_BETWEEN_PHASES}!"
                )
        # Если фазы полуфинала и отборочных существуют, то между началом последнего заплыва отборочных и началом первого заплыва полуфинала должна быть разница во времени
        if (
            self.heats_phase_swims is not None
            and self.semifinals_phase_swims is not None
        ):
            if (
                self.heats_phase_swims[-1].swim_datetime_local_iso
                + MIN_TIME_BETWEEN_PHASES
                > self.semifinals_phase_swims[0].swim_datetime_local_iso
            ):
                raise ValueError(
                    f"Error: difference between last heats swim and first semifinals swim should be not less than {MIN_TIME_BETWEEN_PHASES}!"
                )
        return self


# Класс для дисциплины с результатами
class DisciplineEntryWithResults(DisciplineEntry):
    heats_phase_swims: list[SwimEntryForDisciplineWithSwimmersWithResults] | None = (
        Field(min_length=2, max_length=30)
    )  # От 2 до 30 отборочных заплывов
    finals_phase_swims: list[SwimEntryForDisciplineWithSwimmersWithResults] = Field(
        min_length=1, max_length=30
    )  # От 1 до 30 финалов
    semifinals_phase_swims: (
        list[SwimEntryForDisciplineWithSwimmersWithResults] | None
    ) = Field(
        min_length=2, max_length=2
    )  # Всегда 2 полуфинала


# Создать записи для одного пловца
def create_entries_for_single_swimmer_for_discipline_prediction(
    discipline_data: DisciplineEntry,
    swimmer: SwimmerRaceEntry,
    swim_phase: str,
    swim_number_in_phase: int,
    swims_in_phase: int,
    swim_datetime_local_iso: datetime,
    request: Request,
) -> tuple[list[dict], list[int] | None, list[date] | None, list[int], list[int]]:
    # Вернуть колонки и значения аргументов для графиков: сначала массив для роста,
    # потом для возраста, затем для дорожки. Далее массив с индексом текущего
    # элемента в рамках предсказания
    cur_swimmer_dob = swimmer.dob
    cur_swimmer_height = swimmer.height
    cur_swimmer_lane = swimmer.lane
    rows = []
    cur_element_indices_in_predictions = []
    # Сначала записываем оригинальное предсказание
    row = {
        "race_number_in_phase": swim_number_in_phase,
        "races_in_phase": swims_in_phase,
        "swimmer_age_at_swim_start": (
            calculate_swimmer_age_at_swim_start(swimmer.dob, swim_datetime_local_iso)
        ),
        "swimmer_id": swimmer.id,
        "swimmer_lane": swimmer.lane,
        "swimmer_height": calculate_swimmer_height(swimmer.height),
        "is_swimmer_in_home_country": calculate_is_swimmer_in_home_country(
            swimmer.country_code, discipline_data.host_country_code
        ),
        "swimmer_sex": calculate_swimmer_sex(discipline_data.discipline_sex),
        "distance": discipline_data.discipline_distance,
        "Backstroke": 1 if discipline_data.discipline_style == "Backstroke" else 0,
        "Breaststroke": 1 if discipline_data.discipline_style == "Breaststroke" else 0,
        "Butterfly": 1 if discipline_data.discipline_style == "Butterfly" else 0,
        "Freestyle": 1 if discipline_data.discipline_style == "Freestyle" else 0,
        "Medley": 1 if discipline_data.discipline_style == "Medley" else 0,
        "Africa": 1 if discipline_data.host_region == "Africa" else 0,
        "Americas": 1 if discipline_data.host_region == "Americas" else 0,
        "Asia": 1 if discipline_data.host_region == "Asia" else 0,
        "Europe": 1 if discipline_data.host_region == "Europe" else 0,
        "Oceania": 1 if discipline_data.host_region == "Oceania" else 0,
        "Finals": 1 if swim_phase == "Finals" else 0,
        "Heats": 1 if swim_phase == "Heats" else 0,
        "Semifinals": 1 if swim_phase == "Semifinals" else 0,
        "pool_length": discipline_data.discipline_pool_length,
        "has_race_date_local": 1,
        "race_year": swim_datetime_local_iso.year,
        "race_month_sin": math.sin(2 * math.pi * swim_datetime_local_iso.month / 12),
        "race_month_cos": math.cos(2 * math.pi * swim_datetime_local_iso.month / 12),
        "race_doy_sin": (doy_sin_cos := get_swim_doy_sin_cos(swim_datetime_local_iso))[
            0
        ],
        "race_doy_cos": doy_sin_cos[1],
        "race_dow_sin": math.sin(2 * math.pi * swim_datetime_local_iso.weekday() / 7),
        "race_dow_cos": math.cos(2 * math.pi * swim_datetime_local_iso.weekday() / 7),
        "has_race_time_local": 1,
        "race_time_seconds_sin": (
            seconds_of_day := get_swim_seconds_in_day_sin_cos(swim_datetime_local_iso)
        )[0],
        "race_time_seconds_cos": seconds_of_day[1],
        "has_swimmer_dob": 0 if swimmer.dob is None else 1,
        "swimmer_dob_year": (
            dob_data := calculate_swimmer_dob_year_monthsin_monthcos_doysin_doycos_dowsin_dowcos(
                swim_datetime_local_iso, swimmer.dob
            )
        )[0],
        "swimmer_dob_month_sin": dob_data[1],
        "swimmer_dob_month_cos": dob_data[2],
        "swimmer_dob_doy_sin": dob_data[3],
        "swimmer_dob_doy_cos": dob_data[4],
        "swimmer_dob_dow_sin": dob_data[5],
        "swimmer_dob_dow_cos": dob_data[6],
        "has_swimmer_lane": 1,
        "has_swimmer_height": 0 if swimmer.height is None else 1,
    }
    swimmer_country_embedding = request.app.state.swimmer_country_embedds[
        swimmer.country_code
    ]
    host_country_embedding = request.app.state.host_country_embedds[
        discipline_data.host_country_code
    ]
    swimmer_id_embedding = request.app.state.swimmer_id_embedds[swimmer.id]
    for i in range(8):
        row[f"swimmer_country_{i}"] = swimmer_country_embedding[i]
    for i in range(8):
        row[f"host_country_{i}"] = host_country_embedding[i]
    for i in range(16):
        row[f"swimmer_id_{i}"] = swimmer_id_embedding[i]
    rows.append(row)

    heights = []
    ages = []
    lanes = []
    # Теперь записываем входы для создания предсказаний для графика "зависимость от роста"
    if cur_swimmer_height is not None:
        # От -5 см до +5 см
        indice = -1
        for height_delta in range(-5, 6, 1):
            indice += 1
            rows.append(row.copy())
            rows[-1]["swimmer_height"] = cur_swimmer_height + height_delta
            heights.append(cur_swimmer_height + height_delta)
            if height_delta == 0:
                cur_element_indices_in_predictions.append(indice)
    else:
        heights = None
        cur_element_indices_in_predictions.append(None)

    # Теперь записываем входы для создания предсказаний для графика "зависимость от возраста"
    if cur_swimmer_dob is not None:
        # От -5 лет до +5 лет
        indice = -1
        for age_delta in range(-5, 6, 1):
            indice += 1
            rows.append(row.copy())
            dob_data = calculate_swimmer_dob_year_monthsin_monthcos_doysin_doycos_dowsin_dowcos(
                swim_datetime_local_iso,
                cur_swimmer_dob - relativedelta(years=age_delta),
            )
            rows[-1]["swimmer_age_at_swim_start"] = (
                rows[0]["swimmer_age_at_swim_start"] + age_delta
            )
            rows[-1]["swimmer_dob_year"] = dob_data[0]
            rows[-1]["swimmer_dob_month_sin"] = dob_data[1]
            rows[-1]["swimmer_dob_month_cos"] = dob_data[2]
            rows[-1]["swimmer_dob_doy_sin"] = dob_data[3]
            rows[-1]["swimmer_dob_doy_cos"] = dob_data[4]
            rows[-1]["swimmer_dob_dow_sin"] = dob_data[5]
            rows[-1]["swimmer_dob_dow_cos"] = dob_data[6]
            ages.append(rows[-1]["swimmer_age_at_swim_start"])
            if age_delta == 0:
                cur_element_indices_in_predictions.append(indice)
    else:
        ages = None
        cur_element_indices_in_predictions.append(None)

    # Теперь записиваем входы для создания предсказаний для графика "зависимость от номера дорожки"
    for lane in range(0, 10, 1):
        rows.append(row.copy())
        rows[-1]["swimmer_lane"] = lane
        lanes.append(lane)
        if lane == cur_swimmer_lane:
            cur_element_indices_in_predictions.append(lane)

    return (
        rows,
        heights,
        ages,
        lanes,
        cur_element_indices_in_predictions,
    )


# Дописать словарь для дополнения истории
def append_append_history_dict(
    row_to_append,
    append_history: dict,
    column_preprocessor: ColumnPreprocessorForSinglePhase,
):
    appendice = np.array(
        column_preprocessor.original_preprocessor.scaler_.transform(
            (pd.DataFrame([row_to_append]))[
                column_preprocessor.original_preprocessor.feature_cols
            ]
        )
    ).reshape(1, -1)
    swimmer_id=row_to_append["swimmer_id"]
    if swimmer_id in append_history:
        append_history[swimmer_id] = np.vstack(
            [append_history[swimmer_id], appendice]
        )
    else:
        append_history[swimmer_id] = appendice


@app.post("/disciplinePrediction")
def disciplinePrediction(
    discipline_data: DisciplineEntry, request: Request
) -> DisciplineEntryWithResults:
    append_history_dict = {}

    result_heats_entries = None

    # Предсказываем фазу отборочных
    if discipline_data.heats_phase_swims is not None:
        # Составляем датафрейм
        rows = []
        heights_for_graph_dict: dict[str, list[float]] = {}
        ages_for_graph_dict: dict[str, list[int]] = {}
        lanes_for_graph_dict: dict[str, list[int]] = {}
        indices_for_graphs_dict: dict[str, list[int]] = {}
        for swim_ind, swim in enumerate(discipline_data.heats_phase_swims):
            for swimmer_arr_elem in swim.swimmers_array:
                entry_data = (
                    create_entries_for_single_swimmer_for_discipline_prediction(
                        discipline_data=discipline_data,
                        swimmer=swimmer_arr_elem,
                        swim_phase="Heats",
                        swim_number_in_phase=swim_ind + 1,
                        swims_in_phase=len(discipline_data.heats_phase_swims),
                        swim_datetime_local_iso=swim.swim_datetime_local_iso,
                        request=request,
                    )
                )
                rows.extend(entry_data[0])
                heights_for_graph_dict[swimmer_arr_elem.id] = entry_data[1]
                ages_for_graph_dict[swimmer_arr_elem.id] = entry_data[2]
                lanes_for_graph_dict[swimmer_arr_elem.id] = entry_data[3]
                indices_for_graphs_dict[swimmer_arr_elem.id] = entry_data[4]

        df = pd.DataFrame(rows, columns=DF_COLUMNS_LIST)

        # Получение предсказаний
        predictions = request.app.state.model.predict(
            request.app.state.features_preprocessor_for_single_discipline.transform(
                df, append_history_dict
            )
        )
        # Инверсия масштабирования признаков
        predictions = request.app.state.target_transformer.inverse_transform(
            predictions.reshape(-1, 1)
        ).ravel()

        # Формирование ответа
        predicted_times = []
        for ind in range(len(predictions)):
            # Если поменялся id пловца - значит эта запись - предсказание на введенных пользователем данных, а не для графиков
            swimmer_id = df.iloc[ind]["swimmer_id"]
            if ind == 0 or df.iloc[ind - 1]["swimmer_id"] != swimmer_id:
                predicted_times.append(
                    {
                        "swimmer_id": df.iloc[ind]["swimmer_id"],
                        "race_number_in_phase": df.iloc[ind]["race_number_in_phase"],
                        "predicted_time": float(max(10, predictions[ind])),
                    }
                )
        predicted_times = sorted(predicted_times, key=lambda x: x["predicted_time"])
        from_swimmer_id_to_phase_place = {
            elem["swimmer_id"]: i + 1 for i, elem in enumerate(predicted_times)
        }
        swim_groups_from_swim_number_from_swimmers_ids_to_pred_count={}
        from_swimmer_id_to_swimmer_place_in_swim={}
        for elem in predicted_times:
            if elem['race_number_in_phase'] in swim_groups_from_swim_number_from_swimmers_ids_to_pred_count:
                swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]+=1
            else:
                swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]=1
            from_swimmer_id_to_swimmer_place_in_swim[elem['swimmer_id']]=swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]
        
        result_heats_entries = []
        cur_ind = 0
        for swim_ind, swim in enumerate(discipline_data.heats_phase_swims):
            swimmer_entries_tmp = []
            for swimmer_arr_elem in swim.swimmers_array:
                predicted_time = float(max(10, predictions[cur_ind]))
                append_append_history_dict(
                    row_to_append=rows[cur_ind],
                    append_history=append_history_dict,
                    column_preprocessor=request.app.state.features_preprocessor_for_single_discipline,
                )
                cur_ind += 1
                graph_age_dependency: list[Point] | None = []
                graph_height_dependency: list[Point] | None = []
                graph_lane_dependency: list[Point] = []

                # Формируем массив для графика зависимости от роста
                if heights_for_graph_dict[swimmer_arr_elem.id] is None:
                    graph_height_dependency = None
                else:
                    for i, height in enumerate(
                        heights_for_graph_dict[swimmer_arr_elem.id]
                    ):
                        point_x = height
                        point_y = float(max(10, predictions[cur_ind]))
                        point_is_current_dot = (
                            1
                            if i == indices_for_graphs_dict[swimmer_arr_elem.id][0]
                            else 0
                        )
                        cur_ind += 1
                        graph_height_dependency.append(
                            Point(
                                x=point_x,
                                y=point_y,
                                is_current_dot=point_is_current_dot,
                            )
                        )

                # Формируем массив для графика зависимости от возраста
                if ages_for_graph_dict[swimmer_arr_elem.id] is None:
                    graph_age_dependency = None
                else:
                    for i, age in enumerate(ages_for_graph_dict[swimmer_arr_elem.id]):
                        point_x = age
                        point_y = float(max(10, predictions[cur_ind]))
                        point_is_current_dot = (
                            1
                            if i == indices_for_graphs_dict[swimmer_arr_elem.id][1]
                            else 0
                        )
                        cur_ind += 1
                        graph_age_dependency.append(
                            Point(
                                x=point_x,
                                y=point_y,
                                is_current_dot=point_is_current_dot,
                            )
                        )

                # Формируем массив для графика зависимости от дорожки
                for i, lane in enumerate(lanes_for_graph_dict[swimmer_arr_elem.id]):
                    point_x = lane
                    point_y = float(max(10, predictions[cur_ind]))
                    point_is_current_dot = (
                        1 if i == indices_for_graphs_dict[swimmer_arr_elem.id][2] else 0
                    )
                    cur_ind += 1
                    graph_lane_dependency.append(
                        Point(x=point_x, y=point_y, is_current_dot=point_is_current_dot)
                    )

                swimmer_entries_tmp.append(
                    SwimmerRaceEntryWithResultsForDiscipline(
                        **swimmer_arr_elem.model_dump(),
                        predicted_time=predicted_time,
                        graph_age_dependency=graph_age_dependency,
                        graph_height_dependency=graph_height_dependency,
                        graph_lane_dependency=graph_lane_dependency,
                        predicted_place_in_phase=from_swimmer_id_to_phase_place[
                            swimmer_arr_elem.id
                        ],
                        predicted_place_in_swim=from_swimmer_id_to_swimmer_place_in_swim[swimmer_arr_elem.id]
                    )
                )
            result_heats_entries.append(
                SwimEntryForDisciplineWithSwimmersWithResults(
                    swim_datetime_local_iso=swim.swim_datetime_local_iso,
                    swimmers_array=swimmer_entries_tmp,
                )
            )
    result_semifinals_entries = None
    # Предсказываем фазу полуфинала
    if discipline_data.semifinals_phase_swims is not None:
        if (
            type(discipline_data.semifinals_phase_swims[0])
            == SwimEntryForDisciplineWithSwimmers
        ):
            # Составляем датафрейм
            rows = []
            heights_for_graph_dict: dict[str, list[float]] = {}
            ages_for_graph_dict: dict[str, list[int]] = {}
            lanes_for_graph_dict: dict[str, list[int]] = {}
            indices_for_graphs_dict: dict[str, list[int]] = {}
            for swim_ind, swim in enumerate(discipline_data.semifinals_phase_swims):
                for swimmer_arr_elem in swim.swimmers_array:
                    entry_data = (
                        create_entries_for_single_swimmer_for_discipline_prediction(
                            discipline_data=discipline_data,
                            swimmer=swimmer_arr_elem,
                            swim_phase="Semifinals",
                            swim_number_in_phase=swim_ind + 1,
                            swims_in_phase=len(discipline_data.semifinals_phase_swims),
                            swim_datetime_local_iso=swim.swim_datetime_local_iso,
                            request=request,
                        )
                    )
                    rows.extend(entry_data[0])
                    heights_for_graph_dict[swimmer_arr_elem.id] = entry_data[1]
                    ages_for_graph_dict[swimmer_arr_elem.id] = entry_data[2]
                    lanes_for_graph_dict[swimmer_arr_elem.id] = entry_data[3]
                    indices_for_graphs_dict[swimmer_arr_elem.id] = entry_data[4]

            df = pd.DataFrame(rows, columns=DF_COLUMNS_LIST)

            # Получение предсказаний
            predictions = request.app.state.model.predict(
                request.app.state.features_preprocessor_for_single_discipline.transform(
                    df, append_history_dict
                )
            )
            # Инверсия масштабирования признаков
            predictions = request.app.state.target_transformer.inverse_transform(
                predictions.reshape(-1, 1)
            ).ravel()

            # Формирование ответа
            predicted_times = []
            for ind in range(len(predictions)):
                # Если поменялся id пловца - значит эта запись - предсказание на введенных пользователем данных, а не для графиков
                swimmer_id = df.iloc[ind]["swimmer_id"]
                if ind == 0 or df.iloc[ind - 1]["swimmer_id"] != swimmer_id:
                    predicted_times.append(
                        {
                            "swimmer_id": df.iloc[ind]["swimmer_id"],
                            "race_number_in_phase": df.iloc[ind]["race_number_in_phase"],
                            "predicted_time": float(max(10, predictions[ind])),
                        }
                    )
            predicted_times = sorted(predicted_times, key=lambda x: x["predicted_time"])
            from_swimmer_id_to_phase_place = {
                elem["swimmer_id"]: i + 1 for i, elem in enumerate(predicted_times)
            }
            swim_groups_from_swim_number_from_swimmers_ids_to_pred_count={}
            from_swimmer_id_to_swimmer_place_in_swim={}
            for elem in predicted_times:
                if elem['race_number_in_phase'] in swim_groups_from_swim_number_from_swimmers_ids_to_pred_count:
                    swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]+=1
                else:
                    swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]=1
                from_swimmer_id_to_swimmer_place_in_swim[elem['swimmer_id']]=swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]
            
            result_semifinals_entries = []
            cur_ind = 0
            for swim_ind, swim in enumerate(discipline_data.semifinals_phase_swims):
                swimmer_entries_tmp = []
                for swimmer_arr_elem in swim.swimmers_array:
                    predicted_time = float(max(10, predictions[cur_ind]))
                    append_append_history_dict(
                        row_to_append=rows[cur_ind],
                        append_history=append_history_dict,
                        column_preprocessor=request.app.state.features_preprocessor_for_single_discipline,
                    )
                    cur_ind += 1
                    graph_age_dependency: list[Point] | None = []
                    graph_height_dependency: list[Point] | None = []
                    graph_lane_dependency: list[Point] = []

                    # Формируем массив для графика зависимости от роста
                    if heights_for_graph_dict[swimmer_arr_elem.id] is None:
                        graph_height_dependency = None
                    else:
                        for i, height in enumerate(
                            heights_for_graph_dict[swimmer_arr_elem.id]
                        ):
                            point_x = height
                            point_y = float(max(10, predictions[cur_ind]))
                            point_is_current_dot = (
                                1
                                if i == indices_for_graphs_dict[swimmer_arr_elem.id][0]
                                else 0
                            )
                            cur_ind += 1
                            graph_height_dependency.append(
                                Point(
                                    x=point_x,
                                    y=point_y,
                                    is_current_dot=point_is_current_dot,
                                )
                            )

                    # Формируем массив для графика зависимости от возраста
                    if ages_for_graph_dict[swimmer_arr_elem.id] is None:
                        graph_age_dependency = None
                    else:
                        for i, age in enumerate(
                            ages_for_graph_dict[swimmer_arr_elem.id]
                        ):
                            point_x = age
                            point_y = float(max(10, predictions[cur_ind]))
                            point_is_current_dot = (
                                1
                                if i == indices_for_graphs_dict[swimmer_arr_elem.id][1]
                                else 0
                            )
                            cur_ind += 1
                            graph_age_dependency.append(
                                Point(
                                    x=point_x,
                                    y=point_y,
                                    is_current_dot=point_is_current_dot,
                                )
                            )

                    # Формируем массив для графика зависимости от дорожки
                    for i, lane in enumerate(lanes_for_graph_dict[swimmer_arr_elem.id]):
                        point_x = lane
                        point_y = float(max(10, predictions[cur_ind]))
                        point_is_current_dot = (
                            1
                            if i == indices_for_graphs_dict[swimmer_arr_elem.id][2]
                            else 0
                        )
                        cur_ind += 1
                        graph_lane_dependency.append(
                            Point(
                                x=point_x,
                                y=point_y,
                                is_current_dot=point_is_current_dot,
                            )
                        )

                    swimmer_entries_tmp.append(
                        SwimmerRaceEntryWithResultsForDiscipline(
                            **swimmer_arr_elem.model_dump(),
                            predicted_time=predicted_time,
                            graph_age_dependency=graph_age_dependency,
                            graph_height_dependency=graph_height_dependency,
                            graph_lane_dependency=graph_lane_dependency,
                            predicted_place_in_phase=from_swimmer_id_to_phase_place[
                                swimmer_arr_elem.id
                            ],
                            predicted_place_in_swim=from_swimmer_id_to_swimmer_place_in_swim[swimmer_arr_elem.id]
                        )
                    )
                result_semifinals_entries.append(
                    SwimEntryForDisciplineWithSwimmersWithResults(
                        swim_datetime_local_iso=swim.swim_datetime_local_iso,
                        swimmers_array=swimmer_entries_tmp,
                    )
                )
        elif (
            type(discipline_data.semifinals_phase_swims[0])
            == SwimEntryForDisciplineWithoutSwimmers
        ):
            top_16_swimmers: list[SwimmerRaceEntryWithResultsForDiscipline] = []
            all_swimmers = []
            for swim in result_heats_entries:
                for swimmer in swim.swimmers_array:
                    all_swimmers.append(swimmer)
            top_16_swimmers = sorted(all_swimmers, key=lambda s: s.predicted_time)[:16]

            # Распределяем пловцов по полуфиналам
            seeded_swimmers = [[], []]
            for i, swimmer in enumerate(top_16_swimmers):
                calculated_lane = LANES_SEEDING_INSIDE_SWIM[i // 2]
                seeded_swimmers[(i+1) % 2].append(
                    SwimmerRaceEntry(
                        id=swimmer.id,
                        lane=calculated_lane,
                        country_code=swimmer.country_code,
                        height=swimmer.height,
                        dob=swimmer.dob,
                    )
                )

            seeded_semis = [
                SwimEntryForDisciplineWithSwimmers(
                    swim_datetime_local_iso=discipline_data.semifinals_phase_swims[
                        0
                    ].swim_datetime_local_iso,
                    swimmers_array=seeded_swimmers[0],
                ),
                SwimEntryForDisciplineWithSwimmers(
                    swim_datetime_local_iso=discipline_data.semifinals_phase_swims[
                        1
                    ].swim_datetime_local_iso,
                    swimmers_array=seeded_swimmers[1],
                ),
            ]
            
            # Составляем датафрейм
            rows = []
            heights_for_graph_dict: dict[str, list[float]] = {}
            ages_for_graph_dict: dict[str, list[int]] = {}
            lanes_for_graph_dict: dict[str, list[int]] = {}
            indices_for_graphs_dict: dict[str, list[int]] = {}
            for swim_ind, swim in enumerate(seeded_semis):
                for swimmer_arr_elem in swim.swimmers_array:
                    entry_data = (
                        create_entries_for_single_swimmer_for_discipline_prediction(
                            discipline_data=discipline_data,
                            swimmer=swimmer_arr_elem,
                            swim_phase="Semifinals",
                            swim_number_in_phase=swim_ind + 1,
                            swims_in_phase=len(seeded_semis),
                            swim_datetime_local_iso=swim.swim_datetime_local_iso,
                            request=request,
                        )
                    )
                    rows.extend(entry_data[0])
                    heights_for_graph_dict[swimmer_arr_elem.id] = entry_data[1]
                    ages_for_graph_dict[swimmer_arr_elem.id] = entry_data[2]
                    lanes_for_graph_dict[swimmer_arr_elem.id] = entry_data[3]
                    indices_for_graphs_dict[swimmer_arr_elem.id] = entry_data[4]

            df = pd.DataFrame(rows, columns=DF_COLUMNS_LIST)

            # Получение предсказаний
            predictions = request.app.state.model.predict(
                request.app.state.features_preprocessor_for_single_discipline.transform(
                    df, append_history_dict
                )
            )
            # Инверсия масштабирования признаков
            predictions = request.app.state.target_transformer.inverse_transform(
                predictions.reshape(-1, 1)
            ).ravel()

            # Формирование ответа
            predicted_times = []
            for ind in range(len(predictions)):
                # Если поменялся id пловца - значит эта запись - предсказание на введенных пользователем данных, а не для графиков
                swimmer_id = df.iloc[ind]["swimmer_id"]
                if ind == 0 or df.iloc[ind - 1]["swimmer_id"] != swimmer_id:
                    predicted_times.append(
                        {
                            "swimmer_id": df.iloc[ind]["swimmer_id"],
                            "race_number_in_phase": df.iloc[ind]["race_number_in_phase"],
                            "predicted_time": float(max(10, predictions[ind])),
                        }
                    )
            predicted_times = sorted(predicted_times, key=lambda x: x["predicted_time"])
            from_swimmer_id_to_phase_place = {
                elem["swimmer_id"]: i + 1 for i, elem in enumerate(predicted_times)
            }
            swim_groups_from_swim_number_from_swimmers_ids_to_pred_count={}
            from_swimmer_id_to_swimmer_place_in_swim={}
            for elem in predicted_times:
                if elem['race_number_in_phase'] in swim_groups_from_swim_number_from_swimmers_ids_to_pred_count:
                    swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]+=1
                else:
                    swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]=1
                from_swimmer_id_to_swimmer_place_in_swim[elem['swimmer_id']]=swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]
            
            result_semifinals_entries = []
            cur_ind = 0
            for swim_ind, swim in enumerate(seeded_semis):
                swimmer_entries_tmp = []
                for swimmer_arr_elem in swim.swimmers_array:
                    predicted_time = float(max(10, predictions[cur_ind]))
                    append_append_history_dict(
                        row_to_append=rows[cur_ind],
                        append_history=append_history_dict,
                        column_preprocessor=request.app.state.features_preprocessor_for_single_discipline,
                    )
                    cur_ind += 1
                    graph_age_dependency: list[Point] | None = []
                    graph_height_dependency: list[Point] | None = []
                    graph_lane_dependency: list[Point] = []

                    # Формируем массив для графика зависимости от роста
                    if heights_for_graph_dict[swimmer_arr_elem.id] is None:
                        graph_height_dependency = None
                    else:
                        for i, height in enumerate(
                            heights_for_graph_dict[swimmer_arr_elem.id]
                        ):
                            point_x = height
                            point_y = float(max(10, predictions[cur_ind]))
                            point_is_current_dot = (
                                1
                                if i == indices_for_graphs_dict[swimmer_arr_elem.id][0]
                                else 0
                            )
                            cur_ind += 1
                            graph_height_dependency.append(
                                Point(
                                    x=point_x,
                                    y=point_y,
                                    is_current_dot=point_is_current_dot,
                                )
                            )

                    # Формируем массив для графика зависимости от возраста
                    if ages_for_graph_dict[swimmer_arr_elem.id] is None:
                        graph_age_dependency = None
                    else:
                        for i, age in enumerate(
                            ages_for_graph_dict[swimmer_arr_elem.id]
                        ):
                            point_x = age
                            point_y = float(max(10, predictions[cur_ind]))
                            point_is_current_dot = (
                                1
                                if i == indices_for_graphs_dict[swimmer_arr_elem.id][1]
                                else 0
                            )
                            cur_ind += 1
                            graph_age_dependency.append(
                                Point(
                                    x=point_x,
                                    y=point_y,
                                    is_current_dot=point_is_current_dot,
                                )
                            )

                    # Формируем массив для графика зависимости от дорожки
                    for i, lane in enumerate(lanes_for_graph_dict[swimmer_arr_elem.id]):
                        point_x = lane
                        point_y = float(max(10, predictions[cur_ind]))
                        point_is_current_dot = (
                            1
                            if i == indices_for_graphs_dict[swimmer_arr_elem.id][2]
                            else 0
                        )
                        cur_ind += 1
                        graph_lane_dependency.append(
                            Point(
                                x=point_x,
                                y=point_y,
                                is_current_dot=point_is_current_dot,
                            )
                        )

                    swimmer_entries_tmp.append(
                        SwimmerRaceEntryWithResultsForDiscipline(
                            **swimmer_arr_elem.model_dump(),
                            predicted_time=predicted_time,
                            graph_age_dependency=graph_age_dependency,
                            graph_height_dependency=graph_height_dependency,
                            graph_lane_dependency=graph_lane_dependency,
                            predicted_place_in_phase=from_swimmer_id_to_phase_place[
                                swimmer_arr_elem.id
                            ],
                            predicted_place_in_swim=from_swimmer_id_to_swimmer_place_in_swim[swimmer_arr_elem.id]
                        )
                    )
                result_semifinals_entries.append(
                    SwimEntryForDisciplineWithSwimmersWithResults(
                        swim_datetime_local_iso=swim.swim_datetime_local_iso,
                        swimmers_array=swimmer_entries_tmp,
                    )
                )
    result_finals_entries=None
    # Предсказываем фазу финала
    if discipline_data.finals_phase_swims is not None:
        if type(discipline_data.finals_phase_swims[0]) == SwimEntryForDisciplineWithSwimmers:
            # Составляем датафрейм
            rows = []
            heights_for_graph_dict: dict[str, list[float]] = {}
            ages_for_graph_dict: dict[str, list[int]] = {}
            lanes_for_graph_dict: dict[str, list[int]] = {}
            indices_for_graphs_dict: dict[str, list[int]] = {}
            for swim_ind, swim in enumerate(discipline_data.finals_phase_swims):
                for swimmer_arr_elem in swim.swimmers_array:
                    entry_data = (
                        create_entries_for_single_swimmer_for_discipline_prediction(
                            discipline_data=discipline_data,
                            swimmer=swimmer_arr_elem,
                            swim_phase="Finals",
                            swim_number_in_phase=swim_ind + 1,
                            swims_in_phase=len(discipline_data.finals_phase_swims),
                            swim_datetime_local_iso=swim.swim_datetime_local_iso,
                            request=request,
                        )
                    )
                    rows.extend(entry_data[0])
                    heights_for_graph_dict[swimmer_arr_elem.id] = entry_data[1]
                    ages_for_graph_dict[swimmer_arr_elem.id] = entry_data[2]
                    lanes_for_graph_dict[swimmer_arr_elem.id] = entry_data[3]
                    indices_for_graphs_dict[swimmer_arr_elem.id] = entry_data[4]

            df = pd.DataFrame(rows, columns=DF_COLUMNS_LIST)

            # Получение предсказаний
            predictions = request.app.state.model.predict(
                request.app.state.features_preprocessor_for_single_discipline.transform(
                    df, append_history_dict
                )
            )
            # Инверсия масштабирования признаков
            predictions = request.app.state.target_transformer.inverse_transform(
                predictions.reshape(-1, 1)
            ).ravel()

            # Формирование ответа
            predicted_times = []
            for ind in range(len(predictions)):
                # Если поменялся id пловца - значит эта запись - предсказание на введенных пользователем данных, а не для графиков
                swimmer_id = df.iloc[ind]["swimmer_id"]
                if ind == 0 or df.iloc[ind - 1]["swimmer_id"] != swimmer_id:
                    predicted_times.append(
                        {
                            "swimmer_id": df.iloc[ind]["swimmer_id"],
                            "race_number_in_phase": df.iloc[ind]["race_number_in_phase"],
                            "predicted_time": float(max(10, predictions[ind])),
                        }
                    )
            predicted_times = sorted(predicted_times, key=lambda x: x["predicted_time"])
            from_swimmer_id_to_phase_place = {
                elem["swimmer_id"]: i + 1 for i, elem in enumerate(predicted_times)
            }
            swim_groups_from_swim_number_from_swimmers_ids_to_pred_count={}
            from_swimmer_id_to_swimmer_place_in_swim={}
            for elem in predicted_times:
                if elem['race_number_in_phase'] in swim_groups_from_swim_number_from_swimmers_ids_to_pred_count:
                    swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]+=1
                else:
                    swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]=1
                from_swimmer_id_to_swimmer_place_in_swim[elem['swimmer_id']]=swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]
            
            result_finals_entries = []
            cur_ind = 0
            for swim_ind, swim in enumerate(discipline_data.finals_phase_swims):
                swimmer_entries_tmp = []
                for swimmer_arr_elem in swim.swimmers_array:
                    predicted_time = float(max(10, predictions[cur_ind]))
                    append_append_history_dict(
                        row_to_append=rows[cur_ind],
                        append_history=append_history_dict,
                        column_preprocessor=request.app.state.features_preprocessor_for_single_discipline,
                    )
                    cur_ind += 1
                    graph_age_dependency: list[Point] | None = []
                    graph_height_dependency: list[Point] | None = []
                    graph_lane_dependency: list[Point] = []

                    # Формируем массив для графика зависимости от роста
                    if heights_for_graph_dict[swimmer_arr_elem.id] is None:
                        graph_height_dependency = None
                    else:
                        for i, height in enumerate(
                            heights_for_graph_dict[swimmer_arr_elem.id]
                        ):
                            point_x = height
                            point_y = float(max(10, predictions[cur_ind]))
                            point_is_current_dot = (
                                1
                                if i == indices_for_graphs_dict[swimmer_arr_elem.id][0]
                                else 0
                            )
                            cur_ind += 1
                            graph_height_dependency.append(
                                Point(
                                    x=point_x,
                                    y=point_y,
                                    is_current_dot=point_is_current_dot,
                                )
                            )

                    # Формируем массив для графика зависимости от возраста
                    if ages_for_graph_dict[swimmer_arr_elem.id] is None:
                        graph_age_dependency = None
                    else:
                        for i, age in enumerate(
                            ages_for_graph_dict[swimmer_arr_elem.id]
                        ):
                            point_x = age
                            point_y = float(max(10, predictions[cur_ind]))
                            point_is_current_dot = (
                                1
                                if i == indices_for_graphs_dict[swimmer_arr_elem.id][1]
                                else 0
                            )
                            cur_ind += 1
                            graph_age_dependency.append(
                                Point(
                                    x=point_x,
                                    y=point_y,
                                    is_current_dot=point_is_current_dot,
                                )
                            )

                    # Формируем массив для графика зависимости от дорожки
                    for i, lane in enumerate(lanes_for_graph_dict[swimmer_arr_elem.id]):
                        point_x = lane
                        point_y = float(max(10, predictions[cur_ind]))
                        point_is_current_dot = (
                            1
                            if i == indices_for_graphs_dict[swimmer_arr_elem.id][2]
                            else 0
                        )
                        cur_ind += 1
                        graph_lane_dependency.append(
                            Point(
                                x=point_x,
                                y=point_y,
                                is_current_dot=point_is_current_dot,
                            )
                        )

                    swimmer_entries_tmp.append(
                        SwimmerRaceEntryWithResultsForDiscipline(
                            **swimmer_arr_elem.model_dump(),
                            predicted_time=predicted_time,
                            graph_age_dependency=graph_age_dependency,
                            graph_height_dependency=graph_height_dependency,
                            graph_lane_dependency=graph_lane_dependency,
                            predicted_place_in_phase=from_swimmer_id_to_phase_place[
                                swimmer_arr_elem.id
                            ],
                            predicted_place_in_swim=from_swimmer_id_to_swimmer_place_in_swim[swimmer_arr_elem.id]
                        )
                    )
                result_finals_entries.append(
                    SwimEntryForDisciplineWithSwimmersWithResults(
                        swim_datetime_local_iso=swim.swim_datetime_local_iso,
                        swimmers_array=swimmer_entries_tmp,
                    )
                )
        else:
            top_8_swimmers: list[SwimmerRaceEntryWithResultsForDiscipline] = []
            all_swimmers = []
            if discipline_data.semifinals_phase_swims is not None:
                for swim in result_semifinals_entries:
                    for swimmer in swim.swimmers_array:
                        all_swimmers.append(swimmer)
            else:
                for swim in result_heats_entries:
                    for swimmer in swim.swimmers_array:
                        all_swimmers.append(swimmer)
            top_8_swimmers = sorted(all_swimmers, key=lambda s: s.predicted_time)[:8]

            # Распределяем пловцов по финалу
            seeded_swimmers = [[]]
            for i, swimmer in enumerate(top_8_swimmers):
                calculated_lane = LANES_SEEDING_INSIDE_SWIM[i]
                seeded_swimmers[i % 1].append(
                    SwimmerRaceEntry(
                        id=swimmer.id,
                        lane=calculated_lane,
                        country_code=swimmer.country_code,
                        height=swimmer.height,
                        dob=swimmer.dob,
                    )
                )

            seeded_finals = [
                SwimEntryForDisciplineWithSwimmers(
                    swim_datetime_local_iso=discipline_data.finals_phase_swims[
                        0
                    ].swim_datetime_local_iso,
                    swimmers_array=seeded_swimmers[0],
                ),
            ]
            # Составляем датафрейм
            rows = []
            heights_for_graph_dict: dict[str, list[float]] = {}
            ages_for_graph_dict: dict[str, list[int]] = {}
            lanes_for_graph_dict: dict[str, list[int]] = {}
            indices_for_graphs_dict: dict[str, list[int]] = {}
            for swim_ind, swim in enumerate(seeded_finals):
                for swimmer_arr_elem in swim.swimmers_array:
                    entry_data = (
                        create_entries_for_single_swimmer_for_discipline_prediction(
                            discipline_data=discipline_data,
                            swimmer=swimmer_arr_elem,
                            swim_phase="Finals",
                            swim_number_in_phase=swim_ind + 1,
                            swims_in_phase=len(seeded_finals),
                            swim_datetime_local_iso=swim.swim_datetime_local_iso,
                            request=request,
                        )
                    )
                    rows.extend(entry_data[0])
                    heights_for_graph_dict[swimmer_arr_elem.id] = entry_data[1]
                    ages_for_graph_dict[swimmer_arr_elem.id] = entry_data[2]
                    lanes_for_graph_dict[swimmer_arr_elem.id] = entry_data[3]
                    indices_for_graphs_dict[swimmer_arr_elem.id] = entry_data[4]

            df = pd.DataFrame(rows, columns=DF_COLUMNS_LIST)

            # Получение предсказаний
            predictions = request.app.state.model.predict(
                request.app.state.features_preprocessor_for_single_discipline.transform(
                    df, append_history_dict
                )
            )
            # Инверсия масштабирования признаков
            predictions = request.app.state.target_transformer.inverse_transform(
                predictions.reshape(-1, 1)
            ).ravel()

            # Формирование ответа
            predicted_times = []
            for ind in range(len(predictions)):
                # Если поменялся id пловца - значит эта запись - предсказание на введенных пользователем данных, а не для графиков
                swimmer_id = df.iloc[ind]["swimmer_id"]
                if ind == 0 or df.iloc[ind - 1]["swimmer_id"] != swimmer_id:
                    predicted_times.append(
                        {
                            "swimmer_id": df.iloc[ind]["swimmer_id"],
                            "race_number_in_phase": df.iloc[ind]["race_number_in_phase"],
                            "predicted_time": float(max(10, predictions[ind])),
                        }
                    )
            predicted_times = sorted(predicted_times, key=lambda x: x["predicted_time"])
            from_swimmer_id_to_phase_place = {
                elem["swimmer_id"]: i + 1 for i, elem in enumerate(predicted_times)
            }
            swim_groups_from_swim_number_from_swimmers_ids_to_pred_count={}
            from_swimmer_id_to_swimmer_place_in_swim={}
            for elem in predicted_times:
                if elem['race_number_in_phase'] in swim_groups_from_swim_number_from_swimmers_ids_to_pred_count:
                    swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]+=1
                else:
                    swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]=1
                from_swimmer_id_to_swimmer_place_in_swim[elem['swimmer_id']]=swim_groups_from_swim_number_from_swimmers_ids_to_pred_count[elem['race_number_in_phase']]
            
            result_finals_entries = []
            cur_ind = 0
            for swim_ind, swim in enumerate(seeded_finals):
                swimmer_entries_tmp = []
                for swimmer_arr_elem in swim.swimmers_array:
                    predicted_time = float(max(10, predictions[cur_ind]))
                    append_append_history_dict(
                        row_to_append=rows[cur_ind],
                        append_history=append_history_dict,
                        column_preprocessor=request.app.state.features_preprocessor_for_single_discipline,
                    )
                    cur_ind += 1
                    graph_age_dependency: list[Point] | None = []
                    graph_height_dependency: list[Point] | None = []
                    graph_lane_dependency: list[Point] = []

                    # Формируем массив для графика зависимости от роста
                    if heights_for_graph_dict[swimmer_arr_elem.id] is None:
                        graph_height_dependency = None
                    else:
                        for i, height in enumerate(
                            heights_for_graph_dict[swimmer_arr_elem.id]
                        ):
                            point_x = height
                            point_y = float(max(10, predictions[cur_ind]))
                            point_is_current_dot = (
                                1
                                if i == indices_for_graphs_dict[swimmer_arr_elem.id][0]
                                else 0
                            )
                            cur_ind += 1
                            graph_height_dependency.append(
                                Point(
                                    x=point_x,
                                    y=point_y,
                                    is_current_dot=point_is_current_dot,
                                )
                            )

                    # Формируем массив для графика зависимости от возраста
                    if ages_for_graph_dict[swimmer_arr_elem.id] is None:
                        graph_age_dependency = None
                    else:
                        for i, age in enumerate(
                            ages_for_graph_dict[swimmer_arr_elem.id]
                        ):
                            point_x = age
                            point_y = float(max(10, predictions[cur_ind]))
                            point_is_current_dot = (
                                1
                                if i == indices_for_graphs_dict[swimmer_arr_elem.id][1]
                                else 0
                            )
                            cur_ind += 1
                            graph_age_dependency.append(
                                Point(
                                    x=point_x,
                                    y=point_y,
                                    is_current_dot=point_is_current_dot,
                                )
                            )

                    # Формируем массив для графика зависимости от дорожки
                    for i, lane in enumerate(lanes_for_graph_dict[swimmer_arr_elem.id]):
                        point_x = lane
                        point_y = float(max(10, predictions[cur_ind]))
                        point_is_current_dot = (
                            1
                            if i == indices_for_graphs_dict[swimmer_arr_elem.id][2]
                            else 0
                        )
                        cur_ind += 1
                        graph_lane_dependency.append(
                            Point(
                                x=point_x,
                                y=point_y,
                                is_current_dot=point_is_current_dot,
                            )
                        )

                    swimmer_entries_tmp.append(
                        SwimmerRaceEntryWithResultsForDiscipline(
                            **swimmer_arr_elem.model_dump(),
                            predicted_time=predicted_time,
                            graph_age_dependency=graph_age_dependency,
                            graph_height_dependency=graph_height_dependency,
                            graph_lane_dependency=graph_lane_dependency,
                            predicted_place_in_phase=from_swimmer_id_to_phase_place[
                                swimmer_arr_elem.id
                            ],
                            predicted_place_in_swim=from_swimmer_id_to_swimmer_place_in_swim[swimmer_arr_elem.id]
                        )
                    )
                result_finals_entries.append(
                    SwimEntryForDisciplineWithSwimmersWithResults(
                        swim_datetime_local_iso=swim.swim_datetime_local_iso,
                        swimmers_array=swimmer_entries_tmp,
                    )
                )
    #Склеиваем все полученные результаты в одно предсказание
    return DisciplineEntryWithResults(discipline_sex=discipline_data.discipline_sex,
                                      discipline_distance=discipline_data.discipline_distance,
                                      discipline_style=discipline_data.discipline_style,
                                      discipline_pool_length=discipline_data.discipline_pool_length,
                                      host_country_code=discipline_data.host_country_code,
                                      host_region=discipline_data.host_region,
                                      heats_phase_swims=result_heats_entries,
                                      semifinals_phase_swims=result_semifinals_entries,
                                      finals_phase_swims=result_finals_entries)
