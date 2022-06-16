import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

general_df = pd.read_csv(r'test/general.csv')
prenatal_df = pd.read_csv(r'test/prenatal.csv')
sports_df = pd.read_csv(r'test/sports.csv')


def pd_config():
    pd.set_option('display.max_columns', 8)


def question_1(df):
    hospitals_patients_no = df.hospital.value_counts()
    highes_patients_no = hospitals_patients_no.idxmax()

    print(f"The answer to the 1st question is {highes_patients_no.capitalize()}")


def question_2(df):
    hospitals_patients_no = df.hospital.value_counts()
    general_diagnosis = df.loc[df.hospital == 'general', 'diagnosis'].value_counts()
    general_patients_no = hospitals_patients_no['general']
    stomach_issues = general_diagnosis.loc['stomach']
    share_patients = round((stomach_issues / general_patients_no), 3)

    print(f"The answer to the 2nd question is {share_patients}")


def question_3(df):
    hospitals_patients_no = df.hospital.value_counts()
    sports_diagnosis = df.loc[df.hospital == 'sports', 'diagnosis'].value_counts()
    sports_patients_no = hospitals_patients_no['sports']
    stomach_issues = sports_diagnosis.loc['dislocation']
    share_patients = round((stomach_issues / sports_patients_no), 3)

    print(f"The answer to the 3rd question is {share_patients}")


def question_4(df):
    age_median_general = df.loc[df.hospital == 'general', 'age'].median()
    age_median_sports = df.loc[df.hospital == 'sports', 'age'].median()
    diff_age_median = int(age_median_general - age_median_sports)

    print(f"The answer to the 4th question is {diff_age_median}")


def question_5(df):
    max_blood_tests = df.groupby('hospital', dropna=True).agg({'blood_test': "count"})
    max_blood_test_no = max_blood_tests.max().loc['blood_test']
    max_blood_test_hospital = max_blood_tests.idxmax()[0].capitalize()

    print(f"The answer to the 5th question is {max_blood_test_hospital}, {max_blood_test_no} blood tests")


def answers_1(df):
    question_1(df)
    question_2(df)
    question_3(df)
    question_4(df)
    question_5(df)


def answers_2():
    print("The answer to the 1st question: 15-35")
    print("The answer to the 2nd question: pregnancy")
    print("The answer to the 3rd question: It's because the height recorder in sport hospital is in different"
          "units than meters.")


def histogram(df):
    data = df['age']
    bins = [0, 15, 35, 55, 70, 80]

    plt.hist(data, bins=bins, edgecolor='white', color='orange')
    plt.title("Patient age")
    plt.ylabel("Number of people")
    plt.xlabel("Age")

    plt.show()


def pie_chart(df):
    data = df.diagnosis.value_counts()
    labels = data.index.values
    data = data.values
    explode = [0.01] * len(data)

    plt.pie(data, labels=labels, explode=explode, autopct='%.1f%%')

    plt.show()


def violin(df):
    data_general = df.loc[df.hospital == 'general', 'height']

    data_sports = df.loc[df.hospital == 'sports', 'height']

    data_prenatal = df.loc[df.hospital == 'prenatal', 'height']
    data_list = [data_general, data_sports, data_prenatal]

    fig, axes = plt.subplots()

    axes.set_xticks((1, 2, 3))
    axes.set_xticklabels(("General", "Sports", "Prenatal"))

    plt.violinplot(data_list)

    plt.show()


def main():
    general_df_columns = general_df.columns.values
    prenatal_df.columns = general_df_columns
    sports_df.columns = general_df_columns
    df_united_data = pd.concat([general_df, prenatal_df, sports_df], ignore_index=True)
    df_united_data.drop(columns=["Unnamed: 0"], inplace=True)

    df_united_data.dropna(how='all', inplace=True)

    df_united_data.replace({'woman': 'f', 'female': 'f', 'man': 'm', 'male': 'm'}, inplace=True)

    df_united_data.loc[df_united_data.hospital == 'prenatal', 'gender'] = 'f'

    columns = ["diagnosis", "blood_test", "ecg", "ultrasound", "mri", "xray", "children", "months"]

    for column in columns:
        df_united_data[column].fillna(0, inplace=True)

    df_united_data['blood_test'].replace({'f': np.NaN, 0: np.NaN}, inplace=True)

    # answers_1(df_united_data)

    histogram(df_united_data)
    pie_chart(df_united_data)
    violin(df_united_data)
    answers_2()

    df_united_data.to_excel("my_excel.xlsx")


if "__main__" == __name__:
    main()
