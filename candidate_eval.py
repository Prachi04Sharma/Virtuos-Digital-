import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "#Csefouryears1234",
    database = "hiring_track"
)

cur = db.cursor()
name = input("Student Name: ")
college = input("College Name: ")
r1 = float(input("Round 1 Marks(0-10): "))
r2 = float(input("Round 2 Marks(0-10): "))
r3 = float(input("Round 3 Marks(0-10): "))
tech = float(input("Technical Round Marks(0-20): "))
if len(name) > 30 or len(college) > 50:
    print("Length Error")
    exit()

if not (0 <= r1 <= 10 and 0 <= r2 <= 10 and 0 <= r3 <= 10 and 0 <= tech <= 20):
    print("Range Error")
    exit()

total = r1 + r2 + r3 + tech 
result = "Selected" if total >= 35 else "Rejected" 

cur.execute(
    "INSERT INTO candidate_eval VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NULL)", 
    (name, college, r1, r2, r3, tech, total, result)
)
db.commit()

cur.execute("""
UPDATE candidate_eval c
JOIN (
    SELECT student_name, 
    ROW_NUMBER() OVER (ORDER BY total_marks DESC) r
    FROM candidate_eval 
) t ON c.student_name=t.student_name 
SET c.rank_number=t.r          
""")
db.commit()

cur.execute("SELECT student_name, college_name, total_marks, result, rank_number FROM candidate_eval ORDER BY rank_number")
rows = cur.fetchall()
print("\nName | College | Total | Result | Rank")
for r in rows:
    print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")

cur.close()
db.close()