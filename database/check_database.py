from database.database import Database


db = Database()

print("\n==============================")
print("      DERNIERES MESURES")
print("==============================")

measurements = db.get_measurements(10)

for row in measurements:

    print(row)


print("\n==============================")
print("        DERNIERES ALARMES")
print("==============================")

alarms = db.get_alarms(10)

for row in alarms:

    print(row)