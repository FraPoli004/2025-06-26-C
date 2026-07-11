from database.DB_connect import DBConnect
from model.constructor import Constructor
from model.piazzamento import Piazzamento


class DAO():
    @staticmethod
    def getAllConstructors():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from constructors"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getDDvalue():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.year
                    from seasons s 
                    order by s.year desc"""  # <-- ADATTA colonna e ordine (spesso richiesto)
        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])  # <-- ADATTA nome colonna; valore puro, non oggetto
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes():  # <-- ADATTA parametri
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.*
                    from constructors c 
                    """  # <-- ADATTA; DISTINCT per non duplicare i nodi
        cursor.execute(query)  # <-- un solo parametro: serve comunque la tupla (p,)

        for row in cursor:
            result.append(Constructor(**row))  # <-- le colonne SELECT devono combaciare coi campi della dataclass
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getValoriNodo(c,ai,af):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct replace(r.year,".","") as anno
                    from races r, results r2 
                    where r.raceId = r2.raceId
                    and r2.constructorId = %s
                    and r.year between %s and %s
                    order by anno asc"""                # <-- ADATTA: valore aggregato per singolo nodo
        cursor.execute(query, (c,ai,af))

        for row in cursor:
            result.append(row["anno"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getValoriNodo2(a,c):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct r2.raceId, r2.driverId, r2.position 
                    from races r, results r2 
                    where r.raceId = r2.raceId
                    and r.year = %s
                    and r2.constructorId = %s
                    and r2.position is not null"""  # <-- ADATTA: valore aggregato per singolo nodo
        cursor.execute(query, (a,c))

        for row in cursor:
            result.append(Piazzamento(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(ai,af):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select r.constructorId as idc, count(*) as peso
                    from results r, races ra
                    where r.raceId = ra.raceId
                    and ra.year between %s and %s
                    and r.position is not null
                    group by r.constructorId"""  # <-- ADATTA: valore aggregato per singolo nodo
        cursor.execute(query,(ai,af))

        for row in cursor:
            result.append((row["idc"], row["peso"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesoNull(ai, af):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select r.constructorId as idc, count(*) as peso
                        from results r, races ra
                        where r.raceId = ra.raceId
                        and ra.year between %s and %s
                        group by r.constructorId"""  # <-- ADATTA: valore aggregato per singolo nodo
        cursor.execute(query, (ai, af))

        for row in cursor:
            result.append((row["idc"], row["peso"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(ai,af):  # <-- ADATTA parametri
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct ct1.constructorid as nodo1, ct2.constructorid as nodo2
                    from  (select distinct c.constructorId 
                    from constructors c, results r, races r2 
                    where c.constructorId = r.constructorId and r.raceId = r2.raceId
                    and r2.year between %s and %s) ct1,
                    (select distinct c.constructorId 
                    from constructors c, results r, races r2 
                    where c.constructorId = r.constructorId and r.raceId = r2.raceId
                    and r2.year between %s and %s) ct2
                    where ct1.constructorid < ct2.constructorid 
                    group by ct1.constructorid , ct2.constructorid"""  # <-- ADATTA: peso = COUNT/SUM/AVG...; n1<n2 = coppia una volta sola; GROUP BY solo sui 2 nodi
        cursor.execute(query, (ai,af,ai,af))

        for row in cursor:
            result.append((row["nodo1"], row["nodo2"]))
        cursor.close()
        conn.close()
        return result

