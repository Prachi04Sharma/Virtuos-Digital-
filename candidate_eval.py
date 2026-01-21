import mysql.connector

#Now please also add another logic that the student must score a minimum of 65% in each round to be accepted. This is in addition 
# to 35 marks logic. So a student can fail even if they have scored more than 35 in case they have scored less than 65% in any of the round.  
# If the student has scored 65% in all the rounds, then the student still is rejected as the total is 32.5 which is less than 35.  So the student has to
# fulfil both the requirements 1. Minimum 35 total marks and 2. minimum 65% marks in each individual round.
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "#Csefouryears1234",
    database = "hiring_track"
)

cur = db.cursor()
def get_valid_string(prompt, max_len): 
    while True:
        val = input(prompt)
        if len(val) <= max_len and val.strip() != "": 
            return val
        print(f"Invalid length, enter 1 to {max_len} characters")

def get_valid_number(prompt, l,h):
    while True:
        try:
            val = float(input(prompt))
            if l <= val <= h : 
                return val
            print(f"Out of range ({l}-{h}), Try again")
        except:
            print("Invalid number, enter again.")    
                        
name = get_valid_string("Student Name: ",30) 
college = get_valid_string("College Name: ",50) 
r1 = get_valid_number("Round 1 Marks(0-10): ",0,10)
r2 = get_valid_number("Round 2 Marks(0-10): ",0,10)
r3 = get_valid_number("Round 3 Marks(0-10): ",0,10)
tech = get_valid_number("Tech Round Marks(0-20): ",0,20)


total = r1 + r2 + r3 + tech 
r1_min = r1 >= 0.65 * 10 
r2_min = r2 >= 0.65 * 10 
r3_min = r3 >= 0.65 * 10 
tech_min = tech >= 0.65 * 20
if total >= 35 and r1_min and r2_min and r3_min and tech_min : 
    result = "Selected"
else: 
    result = "Rejected"

cur.execute(
    "INSERT INTO candidate_eval (student_name, college_name, round1_marks, round2_marks, round3_marks, technical_round_marks, total_marks, result, rank_number) VALUES(%s,%s,%s,%s,%s,%s,%s,%s, NULL)",
    (name, college, r1, r2, r3, tech, total, result)
     
)
db.commit()

cur.execute("""
UPDATE candidate_eval c
JOIN (
    SELECT id, 
    DENSE_RANK() OVER (ORDER BY total_marks DESC) r
    FROM candidate_eval 
) t ON c.id=t.id
SET c.rank_number = t.r          
""")
db.commit()

cur.execute("""
SELECT student_name, college_name, round1_marks, round2_marks, round3_marks, technical_round_marks, total_marks, result, rank_number
FROM candidate_eval
ORDER BY rank_number
            """)
rows = cur.fetchall()
print("\nName | College | R1 | R2 | R3| Tech | Total | Result | Rank")
for r in rows:
    print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[8]}")

cur.close()
db.close()