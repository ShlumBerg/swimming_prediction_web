from fastapi.testclient import TestClient
from main import app
import pytest
from datetime import date
from main import MIN_SWIMMER_DOB_DATE, MAX_SWIMMER_DOB_DATE,LANES_SEEDING_INSIDE_SWIM
import re


# Запустить приложение 1 раз на все тестовые классы
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


class TestSwimPrediction:
    def test_swim_prediction_good_1(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 3,
                        "id": "5c04071a-71ad-4a82-929b-3db6a88a1795",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "1999-12-05",
                    },
                    {
                        "lane": 4,
                        "id": "4436920a-0324-4ad2-a4ed-083de6535217",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2002-06-06",
                    },
                    {
                        "lane": 5,
                        "id": "27ea7474-17c5-4696-aea1-dc7b6a51788d",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "2003-12-31",
                    },
                    {
                        "lane": 6,
                        "id": "23b95bf6-16b6-4889-bf28-2e98a2cbef7f",
                        "country_code": "CAN",
                        "height": 176,
                        "dob": "1999-08-11",
                    },
                    {
                        "lane": 7,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2002-03-19",
                    },
                    {
                        "lane": 8,
                        "id": "e8e382a3-eb97-4df2-b6c1-da4cc1434ca5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-05-09",
                    },
                ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        json = responce.json()

        assert "swimmers_array" in json and len(json['swimmers_array'])==8
        for i in json["swimmers_array"]:
            assert i["predicted_time"] >= 10

            # Проверить график зависимости от роста
            assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                isinstance(i["graph_height_dependency"], list)
                and i["height"] is not None
                and len(i["graph_height_dependency"]) == 11
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_height_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
            )

            # Проверить график зависимости от возраста
            assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                isinstance(i["graph_age_dependency"], list)
                and i["dob"] is not None
                and len(i["graph_age_dependency"]) == 11
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_age_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
            )

            # Проверить график зависимости от линии
            assert (
                isinstance(i["graph_lane_dependency"], list)
                and i["lane"] is not None
                and len(i["graph_lane_dependency"]) == 10
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_lane_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
            )
        # Проверить что места пловцов отсортированы в соответствии с временем
        swimmer_entries = sorted(
            json["swimmers_array"], key=lambda x: x["predicted_time"]
        )
        for i in range(len(swimmer_entries) - 1):
            assert (
                swimmer_entries[i]["predicted_place_in_swim"]
                < swimmer_entries[i + 1]["predicted_place_in_swim"]
            )
        # Проверить что места пловцов начинаются с 1 и заканчиваются 8
        assert set(i['predicted_place_in_swim'] for i in json['swimmers_array']) == {1,2,3,4,5,6,7,8}


    def test_swim_prediction_good_check_none_vals(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": 180,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 3,
                        "id": "5c04071a-71ad-4a82-929b-3db6a88a1795",
                        "country_code": None,
                        "height": None,
                        "dob": "1999-12-05",
                    },
                    {
                        "lane": 4,
                        "id": "4436920a-0324-4ad2-a4ed-083de6535217",
                        "country_code": None,
                        "height": None,
                        "dob": None,
                    },
                    {
                        "lane": 5,
                        "id": "27ea7474-17c5-4696-aea1-dc7b6a51788d",
                        "country_code": "NZL",
                        "height": 170,
                        "dob": None,
                    },
                    {
                        "lane": 6,
                        "id": "23b95bf6-16b6-4889-bf28-2e98a2cbef7f",
                        "country_code": None,
                        "height": 176,
                        "dob": "1999-08-11",
                    },
                    {
                        "lane": 7,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": None,
                        "height": 177,
                        "dob": None,
                    },
                    {
                        "lane": 8,
                        "id": "e8e382a3-eb97-4df2-b6c1-da4cc1434ca5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": None,
                    },
                ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        json = responce.json()

        assert "swimmers_array" in json and len(json['swimmers_array'])==8
        for i in json["swimmers_array"]:

            assert i["predicted_time"] >= 10

            # Проверить график зависимости от роста
            assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                isinstance(i["graph_height_dependency"], list)
                and i["height"] is not None
                and len(i["graph_height_dependency"]) == 11
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_height_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
            )

            # Проверить график зависимости от возраста
            assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                isinstance(i["graph_age_dependency"], list)
                and i["dob"] is not None
                and len(i["graph_age_dependency"]) == 11
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_age_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
            )

            # Проверить график зависимости от линии
            assert (
                isinstance(i["graph_lane_dependency"], list)
                and i["lane"] is not None
                and len(i["graph_lane_dependency"]) == 10
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_lane_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
            )
        
        # Проверить что места пловцов отсортированы в соответствии с временем
        swimmer_entries = sorted(
            json["swimmers_array"], key=lambda x: x["predicted_time"]
        )
        for i in range(len(swimmer_entries) - 1):
            assert (
                swimmer_entries[i]["predicted_place_in_swim"]
                < swimmer_entries[i + 1]["predicted_place_in_swim"]
            )
        # Проверить что места пловцов начинаются с 1 и заканчиваются 8
        assert set(i['predicted_place_in_swim'] for i in json['swimmers_array']) == {1,2,3,4,5,6,7,8}

    def test_swim_prediction_good_check_lims_1(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "M",
                "swim_distance": 1500,
                "swim_style": "Backstroke",
                "swim_pool_length": 50,
                "swim_phase": "Semifinals",
                "swim_datetime_local_iso": "2025-01-01T00:00:00",
                "host_country_code": "ISR",
                "host_region": "Africa",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "b72c785c-09af-4549-a5fe-42072944ccf7",
                        "country_code": "CLB",
                        "height": 70,
                        "dob": "1970-01-01",
                    }
                ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        json = responce.json()

        assert "swimmers_array" in json and len(json['swimmers_array'])==1
        for i in json["swimmers_array"]:
            assert i["predicted_time"] >= 10

            # Проверить график зависимости от роста
            assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                isinstance(i["graph_height_dependency"], list)
                and i["height"] is not None
                and len(i["graph_height_dependency"]) == 11
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_height_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
            )

            # Проверить график зависимости от возраста
            assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                isinstance(i["graph_age_dependency"], list)
                and i["dob"] is not None
                and len(i["graph_age_dependency"]) == 11
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_age_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
            )

            # Проверить график зависимости от линии
            assert (
                isinstance(i["graph_lane_dependency"], list)
                and i["lane"] is not None
                and len(i["graph_lane_dependency"]) == 10
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_lane_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
            )
        # Проверить место пловца
        assert json['swimmers_array'][0]['predicted_place_in_swim']==1

    def test_swim_prediction_good_check_lims_2(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 50,
                "swim_style": "Medley",
                "swim_pool_length": 50,
                "swim_phase": "Heats",
                "swim_datetime_local_iso": "2049-12-31T00:00:00",
                "host_country_code": "ISR",
                "host_region": "Africa",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "some_unknown_val",
                        "country_code": "CLB",
                        "height": 300,
                        "dob": "2037-12-31",
                    }
                ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        json = responce.json()

        assert "swimmers_array" in json
        for i in json["swimmers_array"]:
            assert i["predicted_time"] >= 10 and len(json['swimmers_array'])==1

            # Проверить график зависимости от роста
            assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                isinstance(i["graph_height_dependency"], list)
                and i["height"] is not None
                and len(i["graph_height_dependency"]) == 11
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_height_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
            )

            # Проверить график зависимости от возраста
            assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                isinstance(i["graph_age_dependency"], list)
                and i["dob"] is not None
                and len(i["graph_age_dependency"]) == 11
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_age_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
            )

            # Проверить график зависимости от линии
            assert (
                isinstance(i["graph_lane_dependency"], list)
                and i["lane"] is not None
                and len(i["graph_lane_dependency"]) == 10
                and (
                    all(
                        isinstance(j["y"], (int, float))
                        and isinstance(j["x"], (int, float))
                        and isinstance(j["is_current_dot"],int)
                        and j["is_current_dot"] in {0, 1}
                        and j["y"] >= 10
                        for j in i["graph_lane_dependency"]
                    )
                    
                )
                and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
            )
        # Проверить место пловца
        assert json['swimmers_array'][0]['predicted_place_in_swim']==1

    def test_swim_prediction_bad_additional_inputs(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
                "additional_field": "sample_text",
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swim_sex(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": None,
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_sex(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": 1,
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swim_distance(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": None,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_distance(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": "800",
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swim_style(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": None,
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_style(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swim_pool_length(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": None,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_pool_length(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": "25",
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swim_phase(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": None,
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_phase(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": 3,
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swim_datetime(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": None,
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_datetime(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_datetime_2(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40+03:00",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_datetime_3(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2050-01-01T00:00:00",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swim_datetime_4(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2024-12-31T23:59:59",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_host_country_code(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": None,
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_host_country_code(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": 1.12,
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_host_region(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": None,
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_host_region(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Russia",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swimmers_array(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_empty_swimmers_array(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swimmer_lane(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": None,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_lane(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": "1",
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_lane_2(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": -1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_lane_3(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 11,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_duplicate_swimmer_lane(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 1,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_no_swimmer_id(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": None,
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_id(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": 1,
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_country_code(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": 13,
                        "height": None,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_height(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": 13,
                        "height": 69.99,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_height_2(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": 13,
                        "height": 300.01,
                        "dob": "2008-01-22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_duplicate_swimmer_id(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 2,
                        "id": "e2aa25d5-5439-40f0-bace-e5f9c98519fa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_dob(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22T00:00:00",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_dob_2(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008/01/22",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_dob_3(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2025-10-25T12:14:40",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "1969-12-31",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_dob_4(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 800,
                "swim_style": "Freestyle",
                "swim_pool_length": 25,
                "swim_phase": "Finals",
                "swim_datetime_local_iso": "2049-12-31T23:59:59",
                "host_country_code": "CAN",
                "host_region": "Americas",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2050-01-01",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_swimmer_less_than_12_years(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "M",
                "swim_distance": 50,
                "swim_style": "Medley",
                "swim_pool_length": 50,
                "swim_phase": "Heats",
                "swim_datetime_local_iso": "2049-12-31T00:00:00",
                "host_country_code": "ISR",
                "host_region": "Africa",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "b72c785c-09af-4549-a5fe-42072944ccf7",
                        "country_code": "CLB",
                        "height": 300,
                        "dob": "2038-01-01",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_sex(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "F",
                "swim_distance": 50,
                "swim_style": "Medley",
                "swim_pool_length": 50,
                "swim_phase": "Heats",
                "swim_datetime_local_iso": "2049-12-31T00:00:00",
                "host_country_code": "ISR",
                "host_region": "Africa",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "ba0d04f8-904b-47e8-9c68-69efa41bb603",
                        "country_code": "CLB",
                        "height": 300,
                        "dob": "2037-01-01",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422

    def test_swim_prediction_bad_wrong_swimmer_sex_2(self, client):
        responce = client.post(
            "/swimPrediction",
            json={
                "swim_sex": "M",
                "swim_distance": 50,
                "swim_style": "Medley",
                "swim_pool_length": 50,
                "swim_phase": "Heats",
                "swim_datetime_local_iso": "2049-12-31T00:00:00",
                "host_country_code": "ISR",
                "host_region": "Africa",
                "swimmers_array": [
                    {
                        "lane": 1,
                        "id": "601b81fb-d116-41df-a115-1f2e34bbaff2",
                        "country_code": "CLB",
                        "height": 300,
                        "dob": "2037-01-01",
                    }
                ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422


class TestGetSwimmersDict:
    def test_get_swimmers_dict_good_male(self, client):
        responce = client.get(
            "/swimmersDict/M",
        )
        print(responce.json())
        json = responce.json()
        assert responce.status_code == 200

        for key in json:
            swimmer = json[key]
            assert "id" in swimmer
            assert "full_name" in swimmer
            assert "country_code" in swimmer
            assert "height" in swimmer
            assert "dob" in swimmer
            assert "sex" in swimmer

            assert (
                isinstance(swimmer["id"], str)
                and re.match(
                    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                    swimmer["id"],
                )
                and swimmer["id"] == key
            )
            assert isinstance(swimmer["full_name"], str) and swimmer["full_name"] != ""
            assert swimmer["country_code"] is None or (
                isinstance(swimmer["country_code"], str)
                and swimmer["country_code"] != ""
            )
            assert swimmer["height"] is None or isinstance(
                swimmer["height"], (int, float)
            )
            assert swimmer["dob"] is None or (
                isinstance(swimmer["dob"], str)
                and date.fromisoformat(swimmer["dob"]) >= MIN_SWIMMER_DOB_DATE
                and date.fromisoformat(swimmer["dob"]) < MAX_SWIMMER_DOB_DATE
            )
            assert swimmer["sex"] == "M"

    def test_get_swimmers_dict_good_female(self, client):
        responce = client.get(
            "/swimmersDict/F",
        )
        print(responce.json())
        json = responce.json()
        assert responce.status_code == 200

        for key in json:
            swimmer = json[key]
            assert "id" in swimmer
            assert "full_name" in swimmer
            assert "country_code" in swimmer
            assert "height" in swimmer
            assert "dob" in swimmer
            assert "sex" in swimmer

            assert (
                isinstance(swimmer["id"], str)
                and re.match(
                    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                    swimmer["id"],
                )
                and swimmer["id"] == key
            )
            assert isinstance(swimmer["full_name"], str) and swimmer["full_name"] != ""
            assert swimmer["country_code"] is None or (
                isinstance(swimmer["country_code"], str)
                and swimmer["country_code"] != ""
            )
            assert swimmer["height"] is None or isinstance(
                swimmer["height"], (int, float)
            )
            assert swimmer["dob"] is None or (
                isinstance(swimmer["dob"], str)
                and date.fromisoformat(swimmer["dob"]) >= MIN_SWIMMER_DOB_DATE
                and date.fromisoformat(swimmer["dob"]) < MAX_SWIMMER_DOB_DATE
            )
            assert swimmer["sex"] == "F"

    def test_get_swimmers_dict_good_no_intersection(self, client):
        male_resp = client.get(
            "/swimmersDict/M",
        )
        female_resp = client.get(
            "/swimmersDict/F",
        )
        male_dict = male_resp.json()
        female_dict = female_resp.json()
        assert male_resp.status_code == 200
        assert female_resp.status_code == 200
        print(male_dict)
        print(female_dict)
        # Проверить что множества мужчин и женщин не пересекаются
        assert len(set(male_dict.keys()) & set(female_dict.keys())) == 0


class TestDisciplinePrediction:
    def test_discipline_prediction_good_only_finals_1_final_F(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 3,
                        "id": "5c04071a-71ad-4a82-929b-3db6a88a1795",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "1999-12-05",
                    },
                    {
                        "lane": 4,
                        "id": "4436920a-0324-4ad2-a4ed-083de6535217",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2002-06-06",
                    },
                    {
                        "lane": 5,
                        "id": "27ea7474-17c5-4696-aea1-dc7b6a51788d",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "2003-12-31",
                    },
                    {
                        "lane": 6,
                        "id": "23b95bf6-16b6-4889-bf28-2e98a2cbef7f",
                        "country_code": "CAN",
                        "height": 176,
                        "dob": "1999-08-11",
                    },
                    {
                        "lane": 7,
                        "id": "845fb9d3-166e-4046-95a0-73345cccb923",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2002-03-19",
                    },
                    {
                        "lane": 8,
                        "id": "e8e382a3-eb97-4df2-b6c1-da4cc1434ca5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-05-09",
                    },
                    {
                        "lane": 9,
                        "id": "a8ac602e-4d23-4e6c-bfd3-cbba3b2eb8a6",
                        "country_code": "SGP",
                        "height": None,
                        "dob": "2005-12-06",
                    },
                    {
                        "lane": 0,
                        "id": "fab7e9b3-83b6-4c81-bea3-9b70bb78d844",
                        "country_code": "USA",
                        "height": None,
                        "dob": "2005-12-26",
                    },]
                    }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        
        json=responce.json()
        
        assert "heats_swimmers_array" not in json or json["heats_swimmers_array"] is None
        assert "semifinals_swimmers_array" not in json or json["semifinals_swimmers_array"] is None
        assert "finals_phase_swims" in json and len(json['finals_phase_swims'])==1
        for swim in json["finals_phase_swims"]:
            for i in swim["swimmers_array"]:
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 10
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8,9,10}
            
            # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 10
            assert set(i['predicted_place_in_phase'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8,9,10}
        
        #Проверить что места пловцов в фазе отсортированы в соответствии с временем
        phase_times_phaseplaces=[]
        for swim in json['finals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        
    def test_discipline_prediction_good_only_finals_1_final_M(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":100,
                "discipline_style":"Breaststroke",
                "discipline_pool_length":50,
                "host_country_code":"CHN",
                "host_region":"Asia",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 2,
                        "id": "0d72efa4-6c7d-41d9-a827-2e305af7b629",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 3,
                        "id": "0ba01b3a-a13c-427f-8b48-ba12d82e0079",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "1999-12-05",
                    },
                    {
                        "lane": 4,
                        "id": "b79ad305-295a-4bd3-a7e2-a229e6990121",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2002-06-06",
                    },
                    {
                        "lane": 5,
                        "id": "8f78308a-1fee-48b8-857c-e4e71a922d41",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "2003-12-31",
                    },
                    {
                        "lane": 6,
                        "id": "a66bb5a5-6f10-4cfb-9f01-357fa65d9d70",
                        "country_code": "CAN",
                        "height": 176,
                        "dob": "1999-08-11",
                    },
                    {
                        "lane": 7,
                        "id": "1bc6c2a1-4cca-4bd7-a602-92229fbaf090",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2002-03-19",
                    },
                    {
                        "lane": 8,
                        "id": "b9bdb241-f16e-4c37-be4f-93e7bc98d6c5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-05-09",
                    },
                    {
                        "lane": 9,
                        "id": "0dd58198-1d3a-41ea-aaa8-3229c86e21ea",
                        "country_code": "SGP",
                        "height": None,
                        "dob": "2005-12-06",
                    },
                    {
                        "lane": 0,
                        "id": "e8e376d5-5c48-4c80-b9da-461c517d7dfd",
                        "country_code": "USA",
                        "height": None,
                        "dob": "2005-12-26",
                    },]
                    }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        
        json=responce.json()
        
        assert "heats_swimmers_array" not in json or json["heats_swimmers_array"] is None
        assert "semifinals_swimmers_array" not in json or json["semifinals_swimmers_array"] is None
        assert "finals_phase_swims" in json and len(json['finals_phase_swims'])==1
        for swim in json["finals_phase_swims"]:
            for i in swim["swimmers_array"]:
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 10
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8,9,10}
            
            # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 10
            assert set(i['predicted_place_in_phase'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8,9,10}
            
        #Проверить что места пловцов в фазе отсортированы в соответствии с временем
        phase_times_phaseplaces=[]
        for swim in json['finals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
    
    def test_discipline_prediction_good_only_finals_30_finals(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":200,
                "discipline_style":"Butterfly",
                "discipline_pool_length":50,
                "host_country_code":"USA",
                "host_region":"Americas",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "d9a0d620-af1a-4392-a492-3010fa7cc6be",
                        "country_code": None,
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "c048d58a-a95c-4b77-a287-7be2fc58bfce",
                        "country_code": None,
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "233308bc-4b12-4e11-b911-7d6118aed23e",
                        "country_code": None,
                        "height": 180,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "01bf1b7e-2cf7-48d3-b657-f45193e51505",
                        "country_code": None,
                        "height": 180,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d2f039a0-b941-4980-a04c-82e35baaf8d6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "b56a07c5-c180-49cc-84f4-33c3ac7e40c6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "2d3a0b6e-2b3b-429e-8001-77d4c72b21e2",
                        "country_code": "CLB",
                        "height": 178,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "0e97c070-aacd-4ac9-b4d8-8e0c0cd74f01",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "1d90d18e-9e38-46fa-af9c-b7253eecef06",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "79d51968-9ab1-4e31-bb56-8e7c0cae8b6c",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "b72c785c-09af-4549-a5fe-42072944ccf7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "e5312f2e-d574-440e-9bd1-026e8af0bf90",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "422bf785-6510-454e-a15d-7fe0f655561d",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "6e18aae7-7540-4fbc-a528-c45e28b7bcbe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "617fb477-de10-42c5-95d3-9836402ff516",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "1a0be6e5-f2a8-4ed4-a781-405e93d29943",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "ee2827c5-84e3-45f9-97c1-345625f24cc9",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "33e55a56-3ac3-469d-9abe-901e0c8c37ba",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "a3196151-9032-45bb-b0e6-3b7e4085de61",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "17a37ebc-dbe7-45a8-abea-90cee3a498fe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "f688885b-e8d1-41a3-aa0d-574b925d8e9a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "901f270e-ab67-45b0-8729-f65fecb2739a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "94a80afe-b214-4b93-862a-c033fd1bc385",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "dab3cfd0-3608-406c-ac80-e640b11abaca",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d19fc8e0-71e9-47ff-956d-a59ef7dea2e7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "727e7f93-c8be-4093-9fd8-9871175d23d5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "c307f206-181a-44ae-a01c-796e0ff143c5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "3f5d2236-a8c8-422d-9d94-b131fe0e075f",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "5f365d42-61be-4db0-9399-ef509ee1682e",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        
        json=responce.json()
        
        assert "heats_swimmers_array" not in json or json["heats_swimmers_array"] is None
        assert "semifinals_swimmers_array" not in json or json["semifinals_swimmers_array"] is None
        assert "finals_phase_swims" in json and len(json['finals_phase_swims'])==30
        swimmers_places_in_phase=[]
        for swim in json["finals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 1
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1}
            
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 30
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30}
        
        #Проверить что места пловцов в фазе отсортированы в соответствии с временем
        phase_times_phaseplaces=[]
        for swim in json['finals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        
    def test_discipline_prediction_good_1_final_2_semifinals(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":400,
                "discipline_style":"Backstroke",
                "discipline_pool_length":50,
                "host_country_code":"FRA",
                "host_region":"Europe",
                "finals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T11:15:00"}],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 2,
                        "id": "0d72efa4-6c7d-41d9-a827-2e305af7b629",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 3,
                        "id": "274d6b1c-a8bd-45f6-83e8-7b9a4189ba84",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 4,
                        "id": "ccf9e403-4310-44f1-9354-ed1b14ebacb4",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 5,
                        "id": "ab9f017c-fe15-4f90-a1bb-a7354944e906",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 6,
                        "id": "37d5036a-5563-4c39-8ca5-cec7ed0dc77e",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },]
                    },
                    {"swim_datetime_local_iso":"2026-01-22T11:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "132a1067-88d2-4d9e-8d78-6e3cfc6bee40",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "1999-12-05",
                    },
                    {
                        "lane": 4,
                        "id": "54621ba1-b189-4d3f-bb46-bc904b387385",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2002-06-06",
                    },
                    
                    {
                        "lane": 5,
                        "id": "1f0584ce-f7d2-470a-84f9-f36b5da9b2aa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 6,
                        "id": "9f6cbeb2-7f23-4d65-aae9-4d934caf9785",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 7,
                        "id": "b65fa3f3-0e9e-4e46-af27-d54039058752",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 8,
                        "id": "8063865f-b648-406b-81e1-04ea8018594f",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },]
                    }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        
        json=responce.json()
        
        assert "heats_swimmers_array" not in json or json["heats_swimmers_array"] is None
        assert "semifinals_phase_swims" in json and len(json['semifinals_phase_swims'])==2
        assert "finals_phase_swims" in json and len(json['finals_phase_swims'])==1
        swimmers_places_in_phase=[]
        for swim in json["semifinals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 6
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6}
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 12
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8,9,10,11,12}
        swimmers_places_in_phase=[]
        for swim in json["finals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 8
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8}
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 8
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8}
        
        #Проверить что пловцы в финале распределились по дорожкам согласно им местам в полуфинале
        from_swimmer_id_to_lane_in_final={}
        for swim in json['semifinals_phase_swims']:
            for i in swim['swimmers_array']:
                if i['predicted_place_in_phase']<=8:
                    from_swimmer_id_to_lane_in_final[i['id']]=LANES_SEEDING_INSIDE_SWIM[i['predicted_place_in_phase']-1]
        for swim in json['finals_phase_swims']:
            for i in swim['swimmers_array']:
                assert i['lane']==from_swimmer_id_to_lane_in_final[i['id']]
                
        #Проверить что места пловцов в фазе отсортированы в соответствии с временем
        phase_times_phaseplaces=[]
        for swim in json['finals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        phase_times_phaseplaces=[]
        for swim in json['semifinals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
    
    def test_discipline_prediction_good_1_final_2_semifinals_2_heats(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":800,
                "discipline_style":"Medley",
                "discipline_pool_length":50,
                "host_country_code":"RSA",
                "host_region":"Africa",
                "finals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T11:35:00"}],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T11:15:00"},
                                          {"swim_datetime_local_iso":"2026-01-22T11:20:00"}],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "ddbaa713-4412-440c-ab79-e07fd47a8945",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 2,
                        "id": "0d72efa4-6c7d-41d9-a827-2e305af7b629",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 3,
                        "id": "274d6b1c-a8bd-45f6-83e8-7b9a4189ba84",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 4,
                        "id": "ccf9e403-4310-44f1-9354-ed1b14ebacb4",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 5,
                        "id": "ab9f017c-fe15-4f90-a1bb-a7354944e906",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 6,
                        "id": "37d5036a-5563-4c39-8ca5-cec7ed0dc77e",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 7,
                        "id": "8387e7b9-ec8e-4a62-825f-463830529563",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 8,
                        "id": "b8778d67-8241-4ea7-8250-bca5f7e3d1c2",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 9,
                        "id": "99f5fb24-cd48-4d42-8575-777b1d1bbe1f",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },]
                    },
                    {"swim_datetime_local_iso":"2026-01-22T11:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "132a1067-88d2-4d9e-8d78-6e3cfc6bee40",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "1999-12-05",
                    },
                    {
                        "lane": 4,
                        "id": "54621ba1-b189-4d3f-bb46-bc904b387385",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2002-06-06",
                    },
                    
                    {
                        "lane": 5,
                        "id": "1f0584ce-f7d2-470a-84f9-f36b5da9b2aa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 6,
                        "id": "9f6cbeb2-7f23-4d65-aae9-4d934caf9785",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 7,
                        "id": "b65fa3f3-0e9e-4e46-af27-d54039058752",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 8,
                        "id": "8063865f-b648-406b-81e1-04ea8018594f",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 9,
                        "id": "3eee796a-6105-4af4-aeb6-ad0e68c9d6e6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 0,
                        "id": "418b7c24-f0fd-43da-b170-fbaa2c10ea6d",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 1,
                        "id": "d84bb8c1-77e7-4b67-92b3-2e17f4525d1f",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 2,
                        "id": "67d6db85-30d1-45d3-99fc-b8d3b1a8958f",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },]
                    }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        
        json=responce.json()
        
        assert "semifinals_phase_swims" in json and len(json["semifinals_phase_swims"])==2
        assert "heats_phase_swims" in json and len(json['heats_phase_swims'])==2
        assert "finals_phase_swims" in json and len(json['finals_phase_swims'])==1
        swimmers_places_in_phase=[]
        for swim in json["heats_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 10
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8,9,10}
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 20
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}
        swimmers_places_in_phase=[]
        for swim in json["semifinals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 8
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8}
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 16
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}
        swimmers_places_in_phase=[]
        for swim in json["finals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 8
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8}
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 8
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8}
        
        #Проверить что пловцы в финале распределились по дорожкам согласно им местам в полуфинале
        from_swimmer_id_to_lane_in_final={}
        for swim in json['semifinals_phase_swims']:
            for i in swim['swimmers_array']:
                if i['predicted_place_in_phase']<=8:
                    from_swimmer_id_to_lane_in_final[i['id']]=LANES_SEEDING_INSIDE_SWIM[i['predicted_place_in_phase']-1]
        for swim in json['finals_phase_swims']:
            for i in swim['swimmers_array']:
                assert i['lane']==from_swimmer_id_to_lane_in_final[i['id']]
        
        #Проверить что пловцы в полуфинале распределились по дорожкам согласно их местам в отборочных
        from_swimmer_id_to_lane_swim_ind_in_semifinals={}
        for swim in json['heats_phase_swims']:
            for i in swim['swimmers_array']:
                if i['predicted_place_in_phase']<=16:
                    from_swimmer_id_to_lane_swim_ind_in_semifinals[i['id']]=(LANES_SEEDING_INSIDE_SWIM[(i['predicted_place_in_phase']-1)//2],(i['predicted_place_in_phase'])%2)
        for swim_ind,swim in enumerate(json['semifinals_phase_swims']):
            for swimmer in swim['swimmers_array']:
                assert swimmer['lane']==from_swimmer_id_to_lane_swim_ind_in_semifinals[swimmer['id']][0] and \
                    swim_ind==(from_swimmer_id_to_lane_swim_ind_in_semifinals[swimmer['id']][1])
        
        #Проверить что места пловцов в фазе отсортированы в соответствии с временем
        phase_times_phaseplaces=[]
        for swim in json['finals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        phase_times_phaseplaces=[]
        for swim in json['semifinals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        phase_times_phaseplaces=[]
        for swim in json['heats_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        
    def test_discipline_prediction_good_1_final_2_semifinals_30_heats(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":200,
                "discipline_style":"Freestyle",
                "discipline_pool_length":50,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T11:50:00"}],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T11:15:00"},
                                      {"swim_datetime_local_iso":"2026-01-22T11:35:00"}],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "d9a0d620-af1a-4392-a492-3010fa7cc6be",
                        "country_code": None,
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "c048d58a-a95c-4b77-a287-7be2fc58bfce",
                        "country_code": None,
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "233308bc-4b12-4e11-b911-7d6118aed23e",
                        "country_code": None,
                        "height": 180,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "01bf1b7e-2cf7-48d3-b657-f45193e51505",
                        "country_code": None,
                        "height": 180,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d2f039a0-b941-4980-a04c-82e35baaf8d6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "b56a07c5-c180-49cc-84f4-33c3ac7e40c6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "2d3a0b6e-2b3b-429e-8001-77d4c72b21e2",
                        "country_code": "CLB",
                        "height": 178,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "0e97c070-aacd-4ac9-b4d8-8e0c0cd74f01",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "1d90d18e-9e38-46fa-af9c-b7253eecef06",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "79d51968-9ab1-4e31-bb56-8e7c0cae8b6c",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "b72c785c-09af-4549-a5fe-42072944ccf7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "e5312f2e-d574-440e-9bd1-026e8af0bf90",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "422bf785-6510-454e-a15d-7fe0f655561d",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "6e18aae7-7540-4fbc-a528-c45e28b7bcbe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "617fb477-de10-42c5-95d3-9836402ff516",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "1a0be6e5-f2a8-4ed4-a781-405e93d29943",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "ee2827c5-84e3-45f9-97c1-345625f24cc9",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "33e55a56-3ac3-469d-9abe-901e0c8c37ba",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "a3196151-9032-45bb-b0e6-3b7e4085de61",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "17a37ebc-dbe7-45a8-abea-90cee3a498fe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "f688885b-e8d1-41a3-aa0d-574b925d8e9a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "901f270e-ab67-45b0-8729-f65fecb2739a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "94a80afe-b214-4b93-862a-c033fd1bc385",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "dab3cfd0-3608-406c-ac80-e640b11abaca",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d19fc8e0-71e9-47ff-956d-a59ef7dea2e7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "727e7f93-c8be-4093-9fd8-9871175d23d5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "c307f206-181a-44ae-a01c-796e0ff143c5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "3f5d2236-a8c8-422d-9d94-b131fe0e075f",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "5f365d42-61be-4db0-9399-ef509ee1682e",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        
        json=responce.json()
        
        assert "heats_phase_swims" in json and len(json['heats_phase_swims'])==30
        assert "semifinals_phase_swims" in json and len(json['semifinals_phase_swims'])==2
        assert "finals_phase_swims" in json and len(json['finals_phase_swims'])==1
        swimmers_places_in_phase=[]
        for swim in json["heats_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 1
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1}
            
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 30
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30}
        swimmers_places_in_phase=[]
        for swim in json["semifinals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 8
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8}
            
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 16
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16}
        swimmers_places_in_phase=[]
        for swim in json["finals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 8
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8}
            
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 16
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8}
        
        #Проверить что пловцы в финале распределились по дорожкам согласно им местам в полуфинале
        from_swimmer_id_to_lane_in_final={}
        for swim in json['semifinals_phase_swims']:
            for i in swim['swimmers_array']:
                if i['predicted_place_in_phase']<=8:
                    from_swimmer_id_to_lane_in_final[i['id']]=LANES_SEEDING_INSIDE_SWIM[i['predicted_place_in_phase']-1]
        for swim in json['finals_phase_swims']:
            for i in swim['swimmers_array']:
                assert i['lane']==from_swimmer_id_to_lane_in_final[i['id']]
        
        #Проверить что пловцы в полуфинале распределились по дорожкам согласно их местам в отборочных
        from_swimmer_id_to_lane_swim_ind_in_semifinals={}
        for swim in json['heats_phase_swims']:
            for i in swim['swimmers_array']:
                if i['predicted_place_in_phase']<=16:
                    from_swimmer_id_to_lane_swim_ind_in_semifinals[i['id']]=(LANES_SEEDING_INSIDE_SWIM[(i['predicted_place_in_phase']-1)//2],(i['predicted_place_in_phase'])%2)
        for swim_ind,swim in enumerate(json['semifinals_phase_swims']):
            for swimmer in swim['swimmers_array']:
                assert swimmer['lane']==from_swimmer_id_to_lane_swim_ind_in_semifinals[swimmer['id']][0] and \
                    swim_ind==(from_swimmer_id_to_lane_swim_ind_in_semifinals[swimmer['id']][1])
        
        #Проверить что места пловцов в фазе отсортированы в соответствии с временем
        phase_times_phaseplaces=[]
        for swim in json['finals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        phase_times_phaseplaces=[]
        for swim in json['semifinals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        phase_times_phaseplaces=[]
        for swim in json['heats_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        
    def test_discipline_prediction_good_1_final_2_heats(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":1500,
                "discipline_style":"Freestyle",
                "discipline_pool_length":50,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T11:15:00"}],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 2,
                        "id": "0d72efa4-6c7d-41d9-a827-2e305af7b629",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 3,
                        "id": "274d6b1c-a8bd-45f6-83e8-7b9a4189ba84",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 4,
                        "id": "ccf9e403-4310-44f1-9354-ed1b14ebacb4",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 5,
                        "id": "ab9f017c-fe15-4f90-a1bb-a7354944e906",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 6,
                        "id": "37d5036a-5563-4c39-8ca5-cec7ed0dc77e",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },]
                    },
                    {"swim_datetime_local_iso":"2026-01-22T11:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "132a1067-88d2-4d9e-8d78-6e3cfc6bee40",
                        "country_code": "NZL",
                        "height": None,
                        "dob": "1999-12-05",
                    },
                    {
                        "lane": 4,
                        "id": "54621ba1-b189-4d3f-bb46-bc904b387385",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2002-06-06",
                    },
                    
                    {
                        "lane": 5,
                        "id": "1f0584ce-f7d2-470a-84f9-f36b5da9b2aa",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 6,
                        "id": "9f6cbeb2-7f23-4d65-aae9-4d934caf9785",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },
                    {
                        "lane": 7,
                        "id": "b65fa3f3-0e9e-4e46-af27-d54039058752",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    {
                        "lane": 8,
                        "id": "8063865f-b648-406b-81e1-04ea8018594f",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    },]
                    }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        
        json=responce.json()
        
        assert "semifinals_swimmers_array" not in json or json["heats_swimmers_array"] is None
        assert "heats_phase_swims" in json and len(json['heats_phase_swims'])==2
        assert "finals_phase_swims" in json and len(json['finals_phase_swims'])==1
        swimmers_places_in_phase=[]
        for swim in json["heats_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 6
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6}
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 12
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8,9,10,11,12}
        swimmers_places_in_phase=[]
        for swim in json["finals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 8
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8}
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 8
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8}
        
        #Проверить что пловцы в финале распределились по дорожкам согласно им местам в отборочных
        from_swimmer_id_to_lane_in_final={}
        for swim in json['heats_phase_swims']:
            for i in swim['swimmers_array']:
                if i['predicted_place_in_phase']<=8:
                    from_swimmer_id_to_lane_in_final[i['id']]=LANES_SEEDING_INSIDE_SWIM[i['predicted_place_in_phase']-1]
        for swim in json['finals_phase_swims']:
            for i in swim['swimmers_array']:
                assert i['lane']==from_swimmer_id_to_lane_in_final[i['id']]
        
        #Проверить что места пловцов в фазе отсортированы в соответствии с временем
        phase_times_phaseplaces=[]
        for swim in json['finals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        phase_times_phaseplaces=[]
        for swim in json['heats_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        
    def test_discipline_prediction_good_1_final_30_heats(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":200,
                "discipline_style":"Freestyle",
                "discipline_pool_length":50,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T11:15:00"}],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "d9a0d620-af1a-4392-a492-3010fa7cc6be",
                        "country_code": None,
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "c048d58a-a95c-4b77-a287-7be2fc58bfce",
                        "country_code": None,
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "233308bc-4b12-4e11-b911-7d6118aed23e",
                        "country_code": None,
                        "height": 180,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "01bf1b7e-2cf7-48d3-b657-f45193e51505",
                        "country_code": None,
                        "height": 180,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d2f039a0-b941-4980-a04c-82e35baaf8d6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "b56a07c5-c180-49cc-84f4-33c3ac7e40c6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "2d3a0b6e-2b3b-429e-8001-77d4c72b21e2",
                        "country_code": "CLB",
                        "height": 178,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "0e97c070-aacd-4ac9-b4d8-8e0c0cd74f01",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "1d90d18e-9e38-46fa-af9c-b7253eecef06",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "79d51968-9ab1-4e31-bb56-8e7c0cae8b6c",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "b72c785c-09af-4549-a5fe-42072944ccf7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "e5312f2e-d574-440e-9bd1-026e8af0bf90",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "422bf785-6510-454e-a15d-7fe0f655561d",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "6e18aae7-7540-4fbc-a528-c45e28b7bcbe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "617fb477-de10-42c5-95d3-9836402ff516",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "1a0be6e5-f2a8-4ed4-a781-405e93d29943",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "ee2827c5-84e3-45f9-97c1-345625f24cc9",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "33e55a56-3ac3-469d-9abe-901e0c8c37ba",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "a3196151-9032-45bb-b0e6-3b7e4085de61",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "17a37ebc-dbe7-45a8-abea-90cee3a498fe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "f688885b-e8d1-41a3-aa0d-574b925d8e9a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "901f270e-ab67-45b0-8729-f65fecb2739a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "94a80afe-b214-4b93-862a-c033fd1bc385",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "dab3cfd0-3608-406c-ac80-e640b11abaca",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d19fc8e0-71e9-47ff-956d-a59ef7dea2e7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "727e7f93-c8be-4093-9fd8-9871175d23d5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "c307f206-181a-44ae-a01c-796e0ff143c5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "3f5d2236-a8c8-422d-9d94-b131fe0e075f",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "5f365d42-61be-4db0-9399-ef509ee1682e",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 200
        
        json=responce.json()
        
        assert "heats_phase_swims" in json and len(json['heats_phase_swims'])==30
        assert "semifinals_phase_swims" not in json or json['semifinals_phase_swims'] is None
        assert "finals_phase_swims" in json and len(json['finals_phase_swims'])==1
        swimmers_places_in_phase=[]
        for swim in json["heats_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 1
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1}
            
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 30
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30}
        swimmers_places_in_phase=[]
        
        for swim in json["finals_phase_swims"]:
            for i in swim["swimmers_array"]:
                swimmers_places_in_phase.append(i['predicted_place_in_phase'])
                assert i["predicted_time"] >= 10

                # Проверить график зависимости от роста
                assert (i["graph_height_dependency"] is None and i["height"] is None) or (
                    isinstance(i["graph_height_dependency"], list)
                    and i["height"] is not None
                    and len(i["graph_height_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_height_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_height_dependency"]) == 1
                )

                # Проверить график зависимости от возраста
                assert (i["graph_age_dependency"] is None and i["dob"] is None) or (
                    isinstance(i["graph_age_dependency"], list)
                    and i["dob"] is not None
                    and len(i["graph_age_dependency"]) == 11
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_age_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_age_dependency"]) == 1
                )

                # Проверить график зависимости от линии
                assert (
                    isinstance(i["graph_lane_dependency"], list)
                    and i["lane"] is not None
                    and len(i["graph_lane_dependency"]) == 10
                    and (
                        all(
                            isinstance(j["y"], (int, float))
                            and isinstance(j["x"], (int, float))
                            and isinstance(j["is_current_dot"],int)
                            and j["is_current_dot"] in {0, 1}
                            and j["y"] >= 10
                            for j in i["graph_lane_dependency"]
                        )
                        
                    )
                    and sum(j["is_current_dot"] for j in i["graph_lane_dependency"]) == 1
                )
        
            # Проверить что места пловцов отсортированы в соответствии с временем
            swimmer_entries = sorted(
                swim["swimmers_array"], key=lambda x: x["predicted_time"]
            )
            for i in range(len(swimmer_entries) - 1):
                assert (
                    swimmer_entries[i]["predicted_place_in_swim"]
                    < swimmer_entries[i + 1]["predicted_place_in_swim"]
                )
            # Проверить что места пловцов в заплыве начинаются с 1 и заканчиваются 8
            assert set(i['predicted_place_in_swim'] for i in swim['swimmers_array']) == {1,2,3,4,5,6,7,8}
            
        # Проверить что места пловцов в фазе начинаются с 1 и заканчиваются 8
        assert set(swimmers_places_in_phase) == {1,2,3,4,5,6,7,8}
        
        #Проверить что пловцы в финале распределились по дорожкам согласно им местам в отборочных
        from_swimmer_id_to_lane_in_final={}
        for swim in json['heats_phase_swims']:
            for i in swim['swimmers_array']:
                if i['predicted_place_in_phase']<=8:
                    from_swimmer_id_to_lane_in_final[i['id']]=LANES_SEEDING_INSIDE_SWIM[i['predicted_place_in_phase']-1]
        for swim in json['finals_phase_swims']:
            for i in swim['swimmers_array']:
                assert i['lane']==from_swimmer_id_to_lane_in_final[i['id']]
                
        #Проверить что места пловцов в фазе отсортированы в соответствии с временем
        phase_times_phaseplaces=[]
        for swim in json['finals_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
        phase_times_phaseplaces=[]
        for swim in json['heats_phase_swims']:
            for swimmer in swim['swimmers_array']:
                phase_times_phaseplaces.append({"predicted_time":swimmer['predicted_time'],
                            "predicted_place_in_phase":swimmer['predicted_place_in_phase']})
        phase_times_phaseplaces=sorted(phase_times_phaseplaces,key=lambda x:x["predicted_time"])
        for i in range(len(phase_times_phaseplaces) - 1):
                assert (
                    phase_times_phaseplaces[i]["predicted_place_in_phase"]
                    < phase_times_phaseplaces[i + 1]["predicted_place_in_phase"]
                )
    
    def test_discipline_prediction_bad_only_finals_31_final(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":200,
                "discipline_style":"Butterfly",
                "discipline_pool_length":50,
                "host_country_code":"USA",
                "host_region":"Americas",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "d9a0d620-af1a-4392-a492-3010fa7cc6be",
                        "country_code": None,
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "c048d58a-a95c-4b77-a287-7be2fc58bfce",
                        "country_code": None,
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "233308bc-4b12-4e11-b911-7d6118aed23e",
                        "country_code": None,
                        "height": 180,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "01bf1b7e-2cf7-48d3-b657-f45193e51505",
                        "country_code": None,
                        "height": 180,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d2f039a0-b941-4980-a04c-82e35baaf8d6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "b56a07c5-c180-49cc-84f4-33c3ac7e40c6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "2d3a0b6e-2b3b-429e-8001-77d4c72b21e2",
                        "country_code": "CLB",
                        "height": 178,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "0e97c070-aacd-4ac9-b4d8-8e0c0cd74f01",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "1d90d18e-9e38-46fa-af9c-b7253eecef06",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "79d51968-9ab1-4e31-bb56-8e7c0cae8b6c",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "b72c785c-09af-4549-a5fe-42072944ccf7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "e5312f2e-d574-440e-9bd1-026e8af0bf90",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "422bf785-6510-454e-a15d-7fe0f655561d",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "6e18aae7-7540-4fbc-a528-c45e28b7bcbe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "617fb477-de10-42c5-95d3-9836402ff516",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "1a0be6e5-f2a8-4ed4-a781-405e93d29943",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "ee2827c5-84e3-45f9-97c1-345625f24cc9",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "33e55a56-3ac3-469d-9abe-901e0c8c37ba",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "a3196151-9032-45bb-b0e6-3b7e4085de61",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "17a37ebc-dbe7-45a8-abea-90cee3a498fe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "f688885b-e8d1-41a3-aa0d-574b925d8e9a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "901f270e-ab67-45b0-8729-f65fecb2739a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "94a80afe-b214-4b93-862a-c033fd1bc385",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "dab3cfd0-3608-406c-ac80-e640b11abaca",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d19fc8e0-71e9-47ff-956d-a59ef7dea2e7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "727e7f93-c8be-4093-9fd8-9871175d23d5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "c307f206-181a-44ae-a01c-796e0ff143c5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "3f5d2236-a8c8-422d-9d94-b131fe0e075f",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "5f365d42-61be-4db0-9399-ef509ee1682e",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "another_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422
    
    def test_discipline_prediction_bad_only_finals_2_finals_duplicate_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
    
    def test_discipline_prediction_bad_only_finals_2_finals_not_ordered_chronologically(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:59:59",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
    
    def test_discipline_prediction_bad_only_finals_2_finals_wrong_swimmer_sex_1(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_only_finals_2_finals_wrong_swimmer_sex_2(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "a4b41f6c-417c-4ea9-a44b-e2b2fa1fca97",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_only_finals_additional_fields(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "someUnknownField":None,
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_only_finals_empty_finals_array(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_empty_semifinals_array(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "semifinals_phase_swims":[],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_empty_heats_array(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "heats_phase_swims":[],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_with_swimmers_empty_heats_array(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "heats_phase_swims":[],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_2_finals_array_without_swimmers_non_empty_heats_array(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "heats_phase_swims":[],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_heats_array_without_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "heats_phase_swims":[{
                        "swim_datetime_local_iso":"2026-01-22T09:00:00",
                        }],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_semifinals_array_with_swimmers_heats_array_without_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "heats_phase_swims":[{
                        "swim_datetime_local_iso":"2026-01-22T09:00:00",
                        }],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        }
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "6a2eb4b2-576e-468c-a24e-e6d9941415a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_semifinals_array_without_swimmers_heats_array_without_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "heats_phase_swims":[{
                        "swim_datetime_local_iso":"2026-01-22T09:00:00",
                        }],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        }
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_with_swimmers_semifinals_array_without_swimmers_heats_array_with_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "68ca45f7-9c0d-4293-9eb6-1501d3a800a6",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "some_id",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:15:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:15:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_semifinals_array_without_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        }
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:15:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:15:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_with_swimmers_semifinals_array_without_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "some_id",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:15:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:15:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_with_swimmers_heats_array_with_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "some_id",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                    }]}
                    ],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:15:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:15:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "1f26a8f0-0f4f-4b6b-88ee-5ffda4454cf3",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_heats_array_with_swimmers_delay_5_mins_between_phases(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        }
                    ],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "1f26a8f0-0f4f-4b6b-88ee-5ffda4454cf3",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finalssemifinals_array_without_swimmers_heats_array_with_swimmers_delay_5_mins_between_semisheats(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "semifinals_phase_swims":[{
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        },{
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        }],
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:50:00",
                        }
                    ],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "1f26a8f0-0f4f-4b6b-88ee-5ffda4454cf3",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_semifinals_array_with_swimmers_delay_5_mins_between_phases(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:30:00",
                        }
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "1f26a8f0-0f4f-4b6b-88ee-5ffda4454cf3",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_3_semifinals_array_with_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:50:00",
                        }
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "1f26a8f0-0f4f-4b6b-88ee-5ffda4454cf3",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "524d7e8e-8f65-48f4-8565-aba9e14bd114",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]}
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_1_semifinals_array_with_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:50:00",
                        }
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_1_heats_array_with_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:50:00",
                        }
                    ],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
        
    def test_discipline_prediction_bad_1_finals_array_without_swimmers_31_heats_array_with_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"M",
                "discipline_distance":200,
                "discipline_style":"Butterfly",
                "discipline_pool_length":50,
                "host_country_code":"USA",
                "host_region":"Americas",
                "finals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T11:00:00"}],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "some_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "d9a0d620-af1a-4392-a492-3010fa7cc6be",
                        "country_code": None,
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "c048d58a-a95c-4b77-a287-7be2fc58bfce",
                        "country_code": None,
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "233308bc-4b12-4e11-b911-7d6118aed23e",
                        "country_code": None,
                        "height": 180,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "01bf1b7e-2cf7-48d3-b657-f45193e51505",
                        "country_code": None,
                        "height": 180,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d2f039a0-b941-4980-a04c-82e35baaf8d6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "b56a07c5-c180-49cc-84f4-33c3ac7e40c6",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "2d3a0b6e-2b3b-429e-8001-77d4c72b21e2",
                        "country_code": "CLB",
                        "height": 178,
                        "dob": None,
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "0e97c070-aacd-4ac9-b4d8-8e0c0cd74f01",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "1d90d18e-9e38-46fa-af9c-b7253eecef06",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "79d51968-9ab1-4e31-bb56-8e7c0cae8b6c",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "b72c785c-09af-4549-a5fe-42072944ccf7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "e5312f2e-d574-440e-9bd1-026e8af0bf90",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "422bf785-6510-454e-a15d-7fe0f655561d",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "6e18aae7-7540-4fbc-a528-c45e28b7bcbe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "617fb477-de10-42c5-95d3-9836402ff516",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "1a0be6e5-f2a8-4ed4-a781-405e93d29943",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "ee2827c5-84e3-45f9-97c1-345625f24cc9",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "33e55a56-3ac3-469d-9abe-901e0c8c37ba",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "a3196151-9032-45bb-b0e6-3b7e4085de61",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 0,
                        "id": "17a37ebc-dbe7-45a8-abea-90cee3a498fe",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "f688885b-e8d1-41a3-aa0d-574b925d8e9a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "901f270e-ab67-45b0-8729-f65fecb2739a",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "94a80afe-b214-4b93-862a-c033fd1bc385",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "dab3cfd0-3608-406c-ac80-e640b11abaca",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 5,
                        "id": "d19fc8e0-71e9-47ff-956d-a59ef7dea2e7",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 6,
                        "id": "727e7f93-c8be-4093-9fd8-9871175d23d5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 7,
                        "id": "c307f206-181a-44ae-a01c-796e0ff143c5",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 8,
                        "id": "3f5d2236-a8c8-422d-9d94-b131fe0e075f",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "5f365d42-61be-4db0-9399-ef509ee1682e",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:00:00",
                        "swimmers_array":[{
                        "lane": 9,
                        "id": "another_unknown_id",
                        "country_code": "CLB",
                        "height": None,
                        "dob": "2008-01-22",
                    },
                    ]
                    },
                    ],
            },
        )
        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_no_swimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:50:00",
                        }
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinalsnoswimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:50:00",
                        }
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        },
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinals_2_heatsnoswimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:50:00",
                        }
                    ],
                "semifinals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        },
                    ],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:10:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:10:00",
                        },
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_heatsnoswimmers(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:50:00",
                        }
                    ],
                "heats_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:10:00",
                        },
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:10:00",
                        },
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_duplicate_lanes(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinalsduplicatelanes(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:40:00",
                        }
                    ],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinals_2_heatsduplicatelanes(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:50:00"},
                        {"swim_datetime_local_iso":"2026-01-22T09:50:00"},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_heatsduplicatelanes(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_too_early_swim_start_time(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2024-12-31T23:59:59",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 3,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinalstooearlyswimstarttime(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:40:00",
                        }
                    ],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2024-12-31T23:59:59",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2024-12-31T23:59:59",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinals_2_heatstooearlyswimstarttime(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2024-12-31T23:59:59",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2024-12-31T23:59:59",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:50:00"},
                        {"swim_datetime_local_iso":"2026-01-22T09:50:00"},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_heatstooearlyswimstarttime(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2024-12-31T23:59:59",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2024-12-31T23:59:59",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 5,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_too_late_swim_start_time(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2050-01-01T00:00:00",
                        "swimmers_array":[{
                        "lane": 2,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 3,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinalstoolateswimstarttime(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2050-01-01T00:20:00",
                        }
                    ],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2050-01-01T00:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2050-01-01T00:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinals_2_heatstooelateswimstarttime(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2050-01-01T00:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2050-01-01T00:00:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2050-01-01T00:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2050-01-01T00:20:00"},
                        {"swim_datetime_local_iso":"2050-01-01T00:20:00"},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_heatstoolateswimstarttime(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2050-01-01T00:20:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2050-01-01T00:00:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2050-01-01T00:00:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 5,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_too_early_swimmer_dob(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "1969-12-31",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinalstooearlywimmerdob(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:40:00",
                        }
                    ],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "1969-12-31",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinals_2_heatstooearlywimmerdob(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "1969-12-31",
                        }]},],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:50:00"},
                        {"swim_datetime_local_iso":"2026-01-22T09:50:00"},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_heatstooearlywimmerdob(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "1969-12-31",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 5,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_too_late_swimmer_dob(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2050-01-01",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                    ],
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinalstoolatewimmerdob(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:40:00",
                        }
                    ],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2050-01-01",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_semifinals_2_heatstoolatewimmerdob(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T10:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 1,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2050-01-01",
                        },
                        {
                        "lane": 4,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},],
                "semifinals_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:50:00"},
                        {"swim_datetime_local_iso":"2026-01-22T09:50:00"},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422
        
    def test_discipline_prediction_bad_1_finals_2_heatstoolatewimmerdob(self,client):
        responce = client.post(
            "/disciplinePrediction",
            json={
                "discipline_sex":"F",
                "discipline_distance":50,
                "discipline_style":"Freestyle",
                "discipline_pool_length":25,
                "host_country_code":"AUS",
                "host_region":"Oceania",
                "finals_phase_swims":[
                    {
                        "swim_datetime_local_iso":"2026-01-22T09:40:00",
                        }
                    ],
                "heats_phase_swims":[{"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 3,
                        "id": "73c4e2d1-20bc-4406-be0f-34620d5dbc85",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2050-01-01",
                        },
                        {
                        "lane": 2,
                        "id": "7f17b343-bac7-45d5-a4dd-74842b0ac2b1",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},
                        {"swim_datetime_local_iso":"2026-01-22T09:25:00",
                        "swimmers_array":[{
                        "lane": 4,
                        "id": "2ac9b80c-2f1a-4b05-b03e-3f40a1fa08fd",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        },
                        {
                        "lane": 5,
                        "id": "18784db7-e774-4c7c-b78f-f745fb3e8138",
                        "country_code": "AUS",
                        "height": None,
                        "dob": "2005-07-06",
                        }]},]
            },
        )

        print(responce.json())
        assert responce.status_code == 422