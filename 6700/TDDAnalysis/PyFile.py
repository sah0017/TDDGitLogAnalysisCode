"""
Created on Jul 24, 2014

@author: susanha

Used by:
At a class level, determines if a new python file has been found in the git log, and also extracts the python
file name.
Parameters:  when instantiated, receives a path, a file name, and a commit number.
Results:  Contain the code that analyzes the TPP transformations in the commit.
Uses:  Commit

"""
import PyFileCommitDetails
import Method
import re
import Commit
import GitFile
import DeletedLine
import Transformations


class PyFile(object):
    """
    Represents the contents of a python file in a specific commit
    """

    # myTrans = Trans()   # get Transformation static variables and dictionary from Transformation class

    @classmethod
    def python_file_found(self, line):
        eval_line = line.rstrip().lower()
        if (eval_line.startswith("diff")) and (re.search(r"\b\py\b",eval_line)):
            if (re.search(r"\bprod\b", eval_line) or re.search(r"\btest\b",eval_line)
                    or re.search(r"\bsoftwareprocess\b",eval_line) or re.search(r"\brcube\b",eval_line)):
                if not (re.search(r"\b\__init__\b",eval_line)):
                    if not (re.search(r"\bmetadata\b",eval_line)):
                        return True
        elif Commit.Commit.foundNewCommit(eval_line) is True:
            return False
        return False

    @classmethod
    def extract_file_name(self, line):
        str_line = line.rstrip()         # should be on diff line now
        spl_line = str_line.split("/")    # split the line to get the file name, it's in the last element of the list
        path = spl_line[len(spl_line) - 2]
        file_name = spl_line[len(spl_line) - 1]
        return path, file_name

    def __init__(self, path, file_name, commit_nbr):
        """
        Constructor
        """
        self.fileName = file_name
        self.commitNbr = commit_nbr  # this is the commit when it was created
        self.prodFile = self.is_prod_or_test(path, file_name)
        self.commitDetails = []   # a list of pyFileCommitDetail objects on this file in this commit
        self.methods = []         # a list of Method objects in this pyFile
        self.transformations = []

    def analyze_py_file(self, gitfile_handle):
        """Analyzes the information of an individual file within a commit"""
        gitfile_handle.readNextLine() ## either new file mode or index

        my_pyfile_commit_details = self.evaluate_transformations_in_a_file(gitfile_handle)
        self.set_commit_details(my_pyfile_commit_details)
        return my_pyfile_commit_details

    def evaluate_transformations_in_a_file(self, gitfile_handle):
        """Checks the line to see if it is a part of a transformation"""
        added_lines_in_file = 0
        deleted_lines_in_file = 0
        ta_test_lines_in_file = 0
        current_method = Method.Method("Unknown", [])
        method_array = []
        method_indent = 0
        line_with_no_comments = ""

        line = gitfile_handle.readNextLine()

        while self.same_python_file(line):             # have we found a new python file within the same commit?
            prev_line = line_with_no_comments
            line_with_no_comments = self.remove_comments(gitfile_handle)
            no_leading_plus = line_with_no_comments[1:]
            no_leading_spaces = no_leading_plus.strip()
            current_indent = len(no_leading_plus) - len(no_leading_spaces)
            if current_indent <= method_indent and len(no_leading_spaces) > 0:
                current_method = Method.Method("Unknown", [])
                method_array.append(current_method)
            if len(no_leading_spaces) > 0:                 # no need to go through all of this for a blank line
                if no_leading_spaces.startswith("def "):   # Looking for parameters in method call for assignment
                    method_line = True
                    method_indent = len(no_leading_plus) - len(no_leading_spaces)
                    current_method = self.get_method_name_and_parameters(no_leading_spaces)
                    method_array.append(current_method)
                elif line_with_no_comments[0] == "@":   # tells us what class/method the changes are from
                    if re.search("def ", no_leading_spaces):
                        method_name_parts = no_leading_spaces.split("def ")
                        method_name = method_name_parts[1].split("(")
                        current_method.setMethodName(method_name[0])
                        method_array.append(current_method)
                else:
                    method_line = False
                if line_with_no_comments[0] == '-' and line_with_no_comments[1] != '-' and current_method.isATATestCase() is False:
                    # if prodFile:
                    deleted_line = self.process_deleted_line(line_with_no_comments)
                    current_method.addDeletedLine(deleted_line)

                if line_with_no_comments[0] == '+' and line_with_no_comments[1] != '+' and current_method.isATATestCase() is False:
                    # if prodFile:
                    current_method.addedLines = current_method.addedLines + 1
                    self.process_added_line(current_method, method_indent, line_with_no_comments,
                                            prev_line, no_leading_plus, method_line)
            line = gitfile_handle.readNextLine()

        for method in method_array:
            added_lines_in_file = added_lines_in_file + method.getAddedLines()
            deleted_lines_in_file = deleted_lines_in_file + method.getDeletedLines()
            ta_test_lines_in_file = ta_test_lines_in_file + method.getTATestLines()
            # if method.getAddedLines() == 0 and method.getDeletedLines() == 0:
            #        method_array.remove(method)      # empty method
        my_py_file_details = PyFileCommitDetails.PyFileCommitDetails(self.commitNbr,
                                                                     added_lines_in_file, deleted_lines_in_file,
                                                                     ta_test_lines_in_file, method_array)
        return my_py_file_details

    def get_method_name_and_parameters(self, line_with_no_leading_spaces):
        """ Looks for method names and figures out what parameters are part of the method."""
        default_val = False
        params = []
        method_data = line_with_no_leading_spaces.split(" ")   # def in method_data[0], method name in method_data[1] probably with (self, other params in method_data[2-n]
        if len(method_data) > 1:
            method_name = method_data[1].split("(")
            params = method_data[2:]
            if len(params) > 0:
                x = 0
                for parm in params:
                    no_default_val = parm.split("=")
                    if len(no_default_val) > 1:
                        params[x] = no_default_val[0]
                        default_val = True
                    x = x + 1

                if not default_val:
                    last_param = params[len(params) - 1]
                    last_param = last_param[0:len(last_param) - 2]  # removes ): from last parameter
                    params[len(params) - 1] = last_param
                default_val = False
                # print params
            method = Method.Method(method_name[0], params)
            if GitFile.GitFile.TATestCaseDict is not None:
                if method.methodName in GitFile.GitFile.TATestCaseDict:       # if they added one of the TA test cases, the number of lines in the test case will be removed from the number of test case lines that they wrote
                    method.updateTATestLines(GitFile.GitFile.TATestCaseDict[method.methodName])
                    method.setIsTATestCase(True)
        return method

    def process_deleted_line(self, line_with_no_comments):
        deleted_line = DeletedLine.DeletedLine(line_with_no_comments)
        deleted_line.deletedNullValue = self.check_for_deleted_null_value(line_with_no_comments)
        if re.search("return", line_with_no_comments):
            deleted_line.deletedReturn = True
            deleted_line.deletedLiteral = self.check_for_constant_on_return(line_with_no_comments)
        assignment_vars = line_with_no_comments.split("=")     # Check to see if we are assigning a new value to an input parameter
        if len(assignment_vars) > 1:
            assignment_var = assignment_vars[0].strip()
            deleted_line.deletedVariableName = assignment_var
            deleted_line.deletedVariable = True
        if re.search(r"\bif .", line_with_no_comments):
            deleted_line.deletedIf = True
            if_conditional_parts = line_with_no_comments.split("if")
            if_conditional = if_conditional_parts[1].strip()
            deleted_line.deletedIfContents = if_conditional
        if re.search(r"\bwhile .", line_with_no_comments):
            deleted_line.deletedWhile = True
            while_conditional_parts = line_with_no_comments.split("while")
            while_conditional = while_conditional_parts[1].strip()
            deleted_line.deletedWhileContents = while_conditional
        return deleted_line

    def process_added_line(self, current_method, method_indent, line_with_no_comments, prev_line, no_leading_plus, method_line):
        if re.search(r"\bpass\b", line_with_no_comments):      # Transformation 1
            self.add_to_transformation_list(Transformations.Trans.getTransValue("NULL"))
        if current_method.methodName != "Unknown" and not method_line:             # Transformation 9
            my_recurse_search_string = r"\b(?=\w){0}\b(?!\w)\(\)".format(current_method.methodName)
            try:
                if re.search(my_recurse_search_string, line_with_no_comments):
                    if not re.search("if __name__", prev_line):
                        method_line_no_leading_spaces = no_leading_plus.strip()
                        method_line_indent = len(no_leading_plus) - len(method_line_no_leading_spaces)
                        if method_line_indent > method_indent:
                            self.add_to_transformation_list(Transformations.Trans.getTransValue("REC"))
            except Exception as inst:
                print self.fileName, my_recurse_search_string, line_with_no_comments, type(inst)
        if re.search(r"\breturn\b", line_with_no_comments):
            self.process_line_with_return(current_method, line_with_no_comments, no_leading_plus)
        elif re.search(r"\bif.(?!_name__ == \"__main)", line_with_no_comments):
            self.add_to_transformation_list(Transformations.Trans.getTransValue("SF"))
        elif re.search(r"\bwhile\b", line_with_no_comments):
            whileTrans = self.check_while_for_matching_if_or_while(current_method, line_with_no_comments)
            self.add_to_transformation_list(whileTrans)
        elif re.search(r"\bfor\b", no_leading_plus):
            self.add_to_transformation_list(Transformations.Trans.getTransValue("IT"))
        elif re.search(r"\belif\b|\belse\b", no_leading_plus):
            self.add_to_transformation_list(Transformations.Trans.getTransValue("ACase"))
        elif re.search(r"[+/*%\-]|\bmath.\b", no_leading_plus):
            # elif (re.search(r"=",noLeadingPlus)):
            self.add_to_transformation_list(Transformations.Trans.getTransValue("AComp"))
        #    if not (re.search(r"['\"]",noLeadingPlus)):       ## Not Add Computation if the character is inside a quoted string
        #        if not (re.search(r"==",noLeadingPlus)):      ## evaluation, not assignment
        assignment_vars = no_leading_plus.split("=")            # Check to see if we are assigning a new value to an input parameter
        if len(assignment_vars) > 1:
            assignment_var = assignment_vars[0].strip()
            right_side = assignment_vars[1].strip()
            for x in current_method.parameters:
                if x == assignment_var:
                    self.add_to_transformation_list(Transformations.Trans.getTransValue("AS"))
            if right_side.startswith("[") or re.search(r"\bsplit\b", right_side):       # check to see if they created a list
                deleted_variable = self.check_for_deleted_variable(current_method, assignment_var)
                if deleted_variable:
                    self.add_to_transformation_list(Transformations.Trans.getTransValue("VA"))
                else:
                    self.add_to_transformation_list(Transformations.Trans.getTransValue("ArrayNoVar"))

    def process_line_with_return(self, current_method, line_with_no_comments, no_leading_plus):
        rtn_boolean, rtn_value = self.return_with_null(line_with_no_comments)
        deleted_line = self.check_deleted_lines_for_return(current_method)
        if rtn_boolean is True:  # Transformation 1
            self.add_to_transformation_list(Transformations.Trans.getTransValue("NULL"))  # this is either a 'return' or a 'return None'
        elif self.check_for_constant_on_return(rtn_value):  # if there are constants and
            if deleted_line.deletedNullValue == True:   # if there was a Null expression before, they probably did Transformation 2 Null to Constant
                self.add_to_transformation_list(Transformations.Trans.getTransValue("N2C"))
            else:
                self.add_to_transformation_list(Transformations.Trans.getTransValue("ConstOnly"))  # if constants but no previous Null, they probably just went straight to constant
        elif deleted_line.deletedLiteral:       # and the delete section removed a 'return' with a constant
            self.add_to_transformation_list(Transformations.Trans.getTransValue("C2V"))  # then it is probably a Transformation 3 constant to variable
        elif re.search(r"[+/*%\-]|\bmath.\b", no_leading_plus):   # if they're doing math or some math function, it is a Transformation 4 Add Computation.
            self.add_to_transformation_list(Transformations.Trans.getTransValue("AComp"))
        else:
            self.add_to_transformation_list(Transformations.Trans.getTransValue("VarOnly"))  # if we got to this point, they went straight to a variable.
        for parm in current_method.parameters:
            if rtn_value == parm:           # if the return value is a parameter, then it is a Transformation 11 assign.
                self.add_to_transformation_list(Transformations.Trans.getTransValue("AS"))

        # if it wasn't constants on the return
        # this looks for constants after 'return'
    def check_deleted_lines_for_return(self, current_method):
        for dLine in current_method.deletedLines:
            if dLine.deletedReturn:
                return dLine
        return DeletedLine.DeletedLine("")

    def strip_git_action_and_spaces(self, line):
        no_plus = line[1:]
        no_plus = no_plus.strip()
        return no_plus

    def remove_comments(self, git_file_handle):
        line = git_file_handle.getCurrentLine()
        found_quoted_comment = True
        while found_quoted_comment:
            action = line[0]       # either blank space, + or -
            no_plus = self.strip_git_action_and_spaces(line)
            end_comment_found = False
            if no_plus.startswith("'''") or no_plus.startswith("\"\"\""):
                found_quoted_comment = True
                if len(no_plus) > 3 and no_plus.endswith("'''") or no_plus.endswith("\"\"\""):   # one-line comment
                    line = git_file_handle.readNextLine()
                    if line is False:
                        line = ' '
                        found_quoted_comment = False
                    else:
                        end_comment_found = True
                while not end_comment_found:
                    line = git_file_handle.readNextLine()
                    if line is False:
                        line = ' '
                        break
                    no_plus = self.strip_git_action_and_spaces(line)
                    if (line[0] == action) and (line[0] != " "):
                        if no_plus.startswith("'''") or no_plus.startswith("\"\"\"") or no_plus.endswith("'''") or no_plus.endswith("\"\"\""):
                            line = git_file_handle.readNextLine()
                            if line is False:
                                line = ' '
                                found_quoted_comment = False
                            else:
                                end_comment_found = True
                    else:
                        end_comment_found = True
            else:
                found_quoted_comment = False
        if re.search(r"\#", line):
            no_plus = self.strip_git_action_and_spaces(line)
            if no_plus.startswith("#"):
                line_with_no_comments = "\r\n"
            else:
                comment_split = line.split("#")
                line_with_no_comments = comment_split[0]
        else:
            line_with_no_comments = line
        return line_with_no_comments

    def check_while_for_matching_if_or_while(self, current_method, current_line):
        while_conditional_parts = current_line.split("while")
        while_condition = while_conditional_parts[1].strip()
        while_trans = Transformations.Trans.getTransValue("WhileNoIf")
        for d_line in current_method.deletedLines:
            if d_line.deletedIf:
                if while_condition == d_line.deletedIfContents:
                    return Transformations.Trans.getTransValue("I2W")
                else:
                    while_trans = Transformations.Trans.getTransValue("WhileNoIf")
            if d_line.deletedWhile:
                while_trans = self.check_for_constant_to_variable_in_condition(d_line.deletedWhileContents, while_condition)
        return while_trans

    def split_and_clean_condition(self, cond):
        my_split = cond.split(" ")
        if len(my_split) == 3:
            my_first_cond = my_split[0]
            my_cond = my_split[1]
            my_second_cond = my_split[2]
            if my_first_cond.startswith("("):
                my_first_cond = my_first_cond[1:]
            remove_trailing_chars = re.search(r"[a-zA-Z0-9_^):]", my_second_cond)
            if remove_trailing_chars:
                my_second_cond = remove_trailing_chars.group(0)
            return my_first_cond, my_cond, my_second_cond
        else:
            return None, None, None

    def check_for_constant_to_variable_in_condition(self, first_cond, second_cond):
        my_first_if_cond, my_if_cond, my_second_if_cond = self.split_and_clean_condition(first_cond)
        my_first_while_cond, my_while_cond, my_second_while_cond = self.split_and_clean_condition(second_cond)
        if my_first_if_cond is not None:
            if ((my_first_if_cond == my_first_while_cond) and
                (my_if_cond == my_while_cond) and
                (my_second_if_cond.isdigit()) and
                (my_second_while_cond.isalpha())):
                self.add_to_transformation_list(Transformations.Trans.getTransValue("C2V"))
                return Transformations.Trans.getTransValue("I2W")
        return Transformations.Trans.getTransValue("WhileNoIf")

    def same_python_file(self, line):
        " Are we still in the same python file changes or is this a new python file? "
        if line is False:              ## EOF
            line = ''
            return False
        if Commit.Commit.foundNewCommit(line) == True:
            return False
        eval_line = line.rstrip()
        if (eval_line.startswith("diff")):
            return False
        elif (re.search("if __name__", eval_line)):
            return False
        return True

    def check_for_deleted_variable(self, current_method, assignmentVar):
        for dLine in current_method.deletedLines:
            if dLine.deletedVariable:
                if dLine.deletedVariableName == assignmentVar:
                    return dLine.deletedVariableName
        return None

    def check_for_deleted_null_value(self, line):
        deleted_null_value = False
        if line.find("pass") > -1:
            deleted_null_value = True
        rtn_match_obj = re.search("return", line)
        if rtn_match_obj:
            deleted_null_value = self.return_with_null(line)
        return deleted_null_value

    def check_for_constant_on_return(self, line):
        return re.search(r'[0-9]+|[[]]|["]|[\\\']',line)   # if return is followed by a number or [] or " or ', it is probably a constant

    def return_with_null(self, line):
        rtn_boolean = False
        rtn_value = ''
        str_line = line.rstrip()
        spl_line = str_line.split(" ")
        if len(spl_line) > 1:
            rtn_value = spl_line[len(spl_line) - 1]
        if (len(spl_line) == 1) or (rtn_value == 'None'):  # return with no value is basically Null
            rtn_boolean = True
        else:
            rtn_boolean = False
        return rtn_boolean, rtn_value

    def is_prod_or_test(self, path_name, file_name):
        path_name_lower = path_name.lower()
        file_name_lower = file_name.lower()
        prod = False
        if (path_name_lower.startswith('prod') or path_name_lower.startswith('softwareprocess') or
            path_name_lower.startswith('rcube')):
            if not (re.search("test",file_name_lower)):
                prod = True
        return prod

    def is_prod_file(self):
        return self.prodFile

    def get_file_type(self):
        if self.prodFile:
            return "Prod"
        else:
            return "Test"

    def get_file_name(self):
        return self.fileName

    def set_commit_details(self, my_commit_details):
        self.commitDetails.append(my_commit_details)

    def set_method_name(self, method_name):
        my_method = Method.Method(method_name, [])
        self.methods.append(my_method)

    def get_commit_details(self):
        return self.commitDetails

    def number_of_transformations_in_py_file(self):
        nbr_trans = 0
        for i in self.transformations:
            if i >= 0:
                nbr_trans += 1
        return nbr_trans

    def number_of_anti_transformations_in_pyfile(self):
        nbr_anti_trans = 0
        for i in self.transformations:
            if i < 0:
                nbr_anti_trans += 1
        return nbr_anti_trans

    def add_to_transformation_list(self, new_trans):
        self.transformations.append(new_trans)

    def get_transformations(self):
        return self.transformations

    '''
    def isNotSandBoxOrBinaryFile(self, path, fileName):
        pathLower = path.lower();
        if pathLower.startswith('sandbox'):
            notSBFile = False
        else:
            if (re.search(r"\b\pyc\b",fileName)):
                notSBFile = False
            elif (re.search(r"\b\__init__\b",fileName)):
                self.line = GitFile.readNextLine()
                notSBFile = False
            else:
                notSBFile = True
        return notSBFile
    '''

