# student grade checking. 
# Accept the input from the user for Name and Roll Number. 
# Define Three Subjects for the percentage calculation. 
# if percentage is >80 then 1st division
# else percentage is >=60 and <80 then 2nd division. 

def grade_check(): 
    ## Firstly take the input as Name from user. 
    name = input("Please Enter your Name; "); 

    roll_number = input("Please Enter your Roll Number: ")

    student_detail = (name, roll_number); 

    subjects = ["Math", "Science", "Computer"]; 

    d = {}; 

    for subject in subjects: 
        marks = int(input(f"Enter your marks in {subject} : ")); 
        d[subject] = marks; 
    
    value = sum(d.values()); 
    totalPercentage = value / len(subjects); 


    print(f"This is the total percentage: {totalPercentage}")

    print(f"This is the value of dictionary {d}")

    if totalPercentage > 80: 
        print("1st division"); 
    else: 
        print("2nd Division"); 
    # math = input ("Enter your marks in Math: "); 
    # science = input ("Enter your marks in Science: "); 
    # computer = input("Enter your marks in Computer: "); 



    

grade_check(); 