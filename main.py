import os
import glob
import pandas as pd

def get_all_csv_files():
    work_folder = r'/app/table'
    os.chdir(work_folder)
    file_list = glob.glob("*.csv")
    return file_list

def read_all_csv_files(file_list):
    df_list = []
    for file in file_list:
        DataFrame = pd.read_csv(file, encoding='utf_8_sig')
        df_list.append(DataFrame)
    return df_list

def combine_all_dataframes(df_list):
    Result_Dataframe = pd.concat(df_list)
    return Result_Dataframe

def split_data_into_three_parts(Result_Dataframe):
    students = Result_Dataframe[Result_Dataframe['姓名'].notna()][['學號', '姓名', '性別']].drop_duplicates()
    courses = Result_Dataframe[Result_Dataframe['課程名稱'].notna()][['課程編號', '課程名稱', '學分', '教師分機']].drop_duplicates()
    teachers = Result_Dataframe[Result_Dataframe['授課教師'].notna()][['教師分機', '授課教師']].drop_duplicates()
    return (students, courses, teachers)

def combine_courses_and_teachers(courses, teachers):
    courses = courses.merge(teachers, on='教師分機')
    return courses

def combine_students_and_grades(students, grades):
    result = students.merge(grades, on='學號')
    return result

def combine_result_and_courses(result, courses):
    result = result.merge(courses, on='課程編號')
    return result

def get_final_result_file_path():
    result_csv_file_path = '/app/Final_Result.csv'
    return result_csv_file_path

def save_result_to_csv(result, result_csv_file_path):
    result.to_csv(result_csv_file_path, index=False, encoding='utf_8_sig')

def main():
    file_list = get_all_csv_files()
    df_list = read_all_csv_files(file_list)
    Result_Dataframe = combine_all_dataframes(df_list)
    (students, courses, teachers) = split_data_into_three_parts(Result_Dataframe)
    courses = combine_courses_and_teachers(courses, teachers)
    grades = Result_Dataframe[Result_Dataframe['成績'].notna()][['學號', '課程編號', '成績']].drop_duplicates()
    result = combine_students_and_grades(students, grades)
    result = combine_result_and_courses(result, courses)
    result_csv_file_path = get_final_result_file_path()
    save_result_to_csv(result, result_csv_file_path)
    print('finish!')

if __name__ == '__main__':
    main()