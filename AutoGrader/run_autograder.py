"""
1. Get the names of the cpp files from the student submission directory
2. For each of the cpp file, 
    a. Compile the cpp file
    b. Execute the cpp file
    c. Check if the output of the code matches with the expected output
        i. if yes, add the score as 1 in results.json file
        ii. if no, add the score as 0 in results.json file

"""

import subprocess
import json
import os

#STUDENT_SUBMISSION_PATH = "/home/ec2-user/autograder/submission"
#OUTPUT_PATH = "/home/ec2-user/autograder/results/"

STUDENT_SUBMISSION_PATH = "/autograder/submission"
OUTPUT_PATH = "/autograder/results/"
EXPECTED_OUTPUT_FILE = "/autograder/source/expected_outputs.json"

OUTPUT_FILE = "results.json"

if __name__=="__main__":
    #set the generic fields in the results.json file
    results = {}
    results["visibility"] = "after_due_date"
    results["stdout_visibility"] = "visible"
    results["output_format"] = "text"
    results["tests"] = []

    # get the expected outputs from the json file and store in a dictionary
    file_header = open(EXPECTED_OUTPUT_FILE)
    expected_outputs = json.load(file_header)

    #get the list of program files submitted by the student
    files = os.listdir(STUDENT_SUBMISSION_PATH)

    #traverse through each of the files, compile, execute and check if it is pass/fail
    for filename in files:
         
        #set the fields for the particular case in results.json file
        test_result = {}
        test_result["max_score"] = 1
        test_result["visibility"] = "visible"
        test_result["name"] = f"{filename}"
        test_result["name_format"]= "text"
        test_result["output"] = f"Verify execution output for {filename}"
        test_result["output_format"] = "text"

        f = filename.split('.')[0]
        cmds = [ f"g++ -o {f} {filename}", f"./{f}" , f"rm -rf ./{f}"]

        #compile the cpp program
        output = subprocess.run(cmds[0], cwd=STUDENT_SUBMISSION_PATH, capture_output=True, shell=True)
        
        #skip the execution when the compilation fails
        if output.stderr.decode() != "":
            test_result["score"] = 0
            test_result["status"] = "failed"
            results["tests"].append(test_result)
            continue

        #execute the cpp program
        output = subprocess.run(cmds[1], cwd=STUDENT_SUBMISSION_PATH, capture_output=True, shell=True)

        #check if the actual output matches with the expected output
        actual_output = output.stdout.decode()
        print(f"Actual Output: {actual_output} \t Expected Output:{expected_outputs[filename]}")

        if actual_output == expected_outputs[filename]:
            test_result["score"] = 1
            test_result["status"] = "passed"
        else:
            test_result["score"] = 0
            test_result["status"] = "failed"
 
        results["tests"].append(test_result)



    #remove the object file after the end of the program
    output = subprocess.run(cmds[2], cwd=STUDENT_SUBMISSION_PATH, capture_output=True, shell=True)
        
    #store the results of the program execution in results.json file
    with open(OUTPUT_FILE, 'w') as fp:
        json.dump(results, fp)

    # move the results.json file to the specific path as per the requirement from the codegrade
    output_cmd = f"mv {OUTPUT_FILE} {OUTPUT_PATH}{OUTPUT_FILE}"
    output = subprocess.run(output_cmd, capture_output=True, shell=True)

    file_header.close()
