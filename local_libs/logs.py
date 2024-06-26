import json
from datetime import datetime
import os

class logRecorder():

    def __init__(self):

        # Ubicacion de archivos de Logs
        
        # Lee la variable de entorno que indica el entorno actual
        environment = os.getenv('ENVIRONMENT', 'development')  # Por defecto es 'development' si no está configurada

        # Define el project_folder basado en el entorno
        if environment == 'production':
            project_folder = os.path.expanduser('~/infotechonline-dashboard')
        else:
            project_folder = os.path.abspath(os.getcwd())

        self.logs_file = f"{project_folder}/data/logs.json"

        # Se inicializa la funcion get_all_logs
        self.logs_data = self.get_all_logs()

        # Variables necesarias para crear un nuevo registro
        
        self.stagging_product_logs = [] # Almacena todos los productos de un nuevo registro
        self.stagging_log_quantity = 0 # Almacena la cantidad de productos de un nuevo registro

    def get_all_logs(self):

        # Obtener datos de registros de actualizaciónes
        with open(self.logs_file) as f:
            logs_data = json.load(f)

        return logs_data

    def get_logs_by_date(self):

        # Se obtienen todos los registros
        logs_data = self.logs_data

        # Se inicializa la variable que almacenara las actualizaciones del día
        logs_data_today = []

        # Estas variables indican la cantidad de actualizaciones realizadas
        logs_qty = 0
        today_log_qty = 0

        if len(logs_data["logs"]) > 0:

            # Por cada registro dentro del archivo "logs.json"
            for log in logs_data["logs"]:

                # Si la fecha es Hoy
                if log["date"].find(f"{datetime.now().strftime('%Y-%m-%d')}") != -1:
                    
                    today_log_qty+=1
                    # Se almacena dentro de las actualizaciones del día
                    logs_data_today.append(log)

            last_log_date = logs_data["logs"][logs_qty-1]["date"]
        
        else:

            last_log_date = None

        return logs_data_today, today_log_qty, last_log_date
    
    def get_log_quantity(self):

        # Se obtienen todos los registros
        logs_data = self.logs_data

        logs_quantity = 0

        # Por cada registro dentro del archivo "logs.json"
        for log in logs_data["logs"]:

            logs_quantity += 1

        return logs_quantity
    
    def add_product_to_update_log(self, product_id, sku, part_number, stock_status, last_stock_quantity, current_stock_quantity, product_price, final_price, provider, type):

        if provider == "ingram":
            part_number_key = "ingrampartnumber"
        if provider == "intcomex":
            part_number_key = "intcomexsku"

        # Se realiza la estructura del nuevo registro o Log
        product_log = {
            "id": product_id,
            "sku": f"{sku}",
            f"{part_number_key}": part_number,
            "stock": stock_status,
            "last_stock_quantity": last_stock_quantity,
            "current_stock_quantity": current_stock_quantity,
            "past_price": f"{product_price}",
            "regular_price": f"{final_price}",
            "type": type
        }

        self.stagging_product_logs.append(product_log)
        self.stagging_log_quantity += 1

    def add_new_update_log(self):

        # Se guardan los registros dentro de "logs.json"
        with open(self.logs_file) as f:

            logs_data = json.load(f)
            logs_data_list = logs_data["logs"]

            error_quantity = 0
            for product in self.stagging_product_logs:
                if product["type"] == "error":
                    error_quantity += 1

            # Se realiza la estructura del log con la fecha de actualización, cantidad de productos y el detalle de cada producto actualizado
            new_log = {
                "date": f"{datetime.now().strftime('%Y-%m-%d')} / {datetime.now().time().strftime('%H:%M:%S')}",
                "type": "Update",
                "qty": self.stagging_log_quantity,
                "products": self.stagging_product_logs,
                "error_quantity": error_quantity
            }

            logs_data_list.append(new_log)
            logs_data["logs"] = logs_data_list
            log = json.dumps(logs_data, indent=4)
        
        # Se escriben los datos dentro del archivo
        with open(self.logs_file, 'w') as file:
            file.write(log)

    def add_new_product_log(self, woo_product_id, product_sku, part_number, stock, price):

        # Se guarda el registro dentro de "logs.json"
        with open(self.logs_file) as f:

            logs_data = json.load(f)
            logs_data_list = logs_data["logs"]

            # Estructura del Log de tipo "Add"
            new_log = {
                "date": f"{datetime.now().strftime('%Y-%m-%d')} / {datetime.now().time().strftime('%H:%M:%S')}",
                "type": "Add",
                "qty": 1,
                "products": [{
                    "id": woo_product_id,
                    "sku": product_sku,
                    "ingrampartnumber": part_number,
                    "stock": stock,
                    "past_price": price,
                    "regular_price": price
                }]
            }

            logs_data_list.append(new_log)
            logs_data["logs"] = logs_data_list
            log = json.dumps(logs_data, indent=4)

        # Se escribe el nuevo Log
        with open(self.logs_file, 'w') as file:
            file.write(log)


if __name__ == '__main__':

    logs = logRecorder()

    print(logs.get_all_logs())
    print(logs.get_logs_by_date()[0], logs.get_logs_by_date()[1], logs.get_logs_by_date()[2])
