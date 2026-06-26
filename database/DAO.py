from database.DB_connect import DBConnect
from model.Product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCategorie():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT DISTINCT c.category_name FROM categories c"

        cursor.execute(query)

        for row in cursor:
            results.append(row["category_name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(categoria):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT p.product_id, p.product_name
                    FROM categories c, products p 
                    where p.category_id = c.category_id 
                    and c.category_name = %s
                    group by p.product_id"""

        cursor.execute(query, (categoria,))

        for row in cursor:
            results.append(Product(row["product_id"], row["product_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllCoppie(anno1, anno2, categoria, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT p1.product_id as id1, p2.product_id as id2
                    FROM products p1, products p2, order_items oi1, order_items oi2,
                    orders o1, orders o2, categories c 
                    where p1.product_id = oi1.product_id 
                    and oi1.order_id = o1.order_id 
                    and p2.product_id = oi2.product_id 
                    and oi2.order_id = o2.order_id
                    and c.category_id = p1.category_id 
                    and c.category_id = p2.category_id 
                    and o1.order_date between %s and %s
                    and o2.order_date between %s and %s
                    and p1.product_id < p2.product_id 
                    and c.category_name = %s
                    group by p1.product_id, p2.product_id"""

        cursor.execute(query, (anno1, anno2, anno1, anno2, categoria))

        for row in cursor:
            c1 = idMap[row["id1"]]
            c2 = idMap[row["id2"]]
            results.append((c1, c2))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getVendite(anno1, anno2, categoria, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select p.product_id as id, sum(oi.quantity) as peso
                    from products p, order_items oi, orders o, categories c  
                    where p.product_id = oi.product_id 
                    and oi.order_id = o.order_id 
                    and p.category_id = c.category_id 
                    and o.order_date between %s and %s
                    and c.category_name = %s
                    group by p.product_id """

        cursor.execute(query, (anno1, anno2, categoria))

        for row in cursor:
            c1 = idMap[row["id"]]
            peso = row["peso"]
            results.append((c1, peso))

        cursor.close()
        conn.close()
        return results
