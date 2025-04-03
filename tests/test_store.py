import requests
import allure
import pytest

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_create_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, (f"Ожидался статус 200, а получен {response.status_code}")

        with (allure.step("Проверка данных в ответе")):
            assert response_json["id"] == payload["id"], "id заказа не совпадает"
            assert response_json["petId"] == payload["petId"], "petId не совпадает"
            assert response_json["quantity"] == payload["quantity"], "quantity не совпадает"
            assert response_json["status"] == payload["status"], "status не совпадает"
            assert response_json["complete"] == payload["complete"], "complete не совпадает"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order(self):
        order_id = 1

        with allure.step(f"Отправка запроса на получение информации о заказе с ID {order_id}"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных в ответе"):
            assert response.status_code == 200, (f"Ошибка: ожидался статус 200, а получен {response.status_code}")
            assert response_json["id"] == order_id, "ID заказа не совпадает"

    @allure.title("Удаление заказа по ID")
    def test_delete_order(self):
        order_id = 1

        with allure.step(f"Отправка запроса на удаление заказа с ID {order_id}"):
            response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 200, "Ожидался статус 200"

        with allure.step(f"Отправка запроса на получение заказа с ID {order_id}"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404, "Ожидался статус 404 после удаления заказа"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        order_id = 9999

        with allure.step(f"Отправка запроса на получение заказа с ID {order_id}"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404, "Ожидался статус 404"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря магазина"):
            response = requests.get(url=f"{BASE_URL}/store/inventory")
            assert response.status_code == 200, "Ожидался статус 200"

            inventory_data = response.json()
            assert isinstance(inventory_data, dict), "Ожидался формат словаря"
            assert isinstance(inventory_data["approved"], int), "Значение 'approved' должно быть целым числом"
            assert isinstance(inventory_data["delivered"], int), "Значение 'delivered' должно быть целым числом"
