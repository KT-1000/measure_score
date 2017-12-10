import argparse
import pandas as pd

MEASURES = {'AMI', 'COPD', 'HF', 'HWR', 'PN', 'THA-TKA'}

DIAGNOSIS_CODES = {'AMI': ['410.00', '410.01', '410.10', '410.11', '410.20', '410.21', '410.30', '410.31', '410.40',
                           '410.41', '410.50', '410.51', '410.60', '410.61', '410.70', '410.71', '410.80', '410.81',
                           '410.90', '410.91'],
                   'COPD': ['491.21', '491.22', '491.8', '491.9', '492.8', '493.20', '493.21', '493.22', '496',
                            '518.81', '518.82', '518.84', '799.1'],
                   'HF': ['402.01', '402.11', '402.91', '404.01', '404.03', '404.11', '404.13', '404.91', '404.93',
                          '428.xx'],
                   'HWR': ['CCS'],
                   'PN': ['480.0', '480.1', '480.2', '480.3', '480.8', '480.9', '481', '482.0', '482.1', '482.2',
                          '482.30', '482.31', '482.32', '482.39', '482.40', '482.41', '482.42', '482.49', '482.81',
                          '482.82', '482.83', '482.84', '482.89', '482.9', '483.0', '483.1', '483.8', '485', '486',
                          '487.0', '488.11'],
                   'THA-TKA': ['81.51', '81.54']
                   }

COMORBIDITY_CODES = {'AMI': ['HistoryofPTCA', 'HistoryofCABG', 'Congestiveheartfailure', 'Acutecoronarysyndrome',
                             'Anteriormyocardialinfarction', 'Otherlocationofmyocardialinfarction',
                             'Anginapectorisoldmyocardialinfarction', 'Coronaryatherosclerosis',
                             'Valvularorrheumaticheartdisease', 'Specifiedarrhythmias', 'Historyofinfection',
                             'Metastaticcanceroracuteleukemia', 'Cancer', 'Diabetesmellitus(DM)orDMcomplications',
                             'Protein-caloriemalnutrition', 'Disordersoffluidelectrolyteacid-base',
                             'Irondeficiencyorotheranemiasandblooddisease', 'Dementiaorotherspecifiedbraindisorders',
                             'Hemiplegiaparaplegiaparalysisfunctionaldisability', 'Stroke', 'Cerebrovasculardisease',
                             'Vascularorcirculatorydisease', 'Chronicobstructivepulmonarydisease', 'Asthma',
                             'Pneumonia', 'End-stagerenaldiseaseordialysis', 'Renalfailure',
                             'Otherurinarytractdisorders', 'Decubitusulcerorchronicskinulcer'
                             ],
                     'COPD': ['HistoryofMechanicalVentilation', 'SleepApnea', 'Respiratordependence/tracheostomystatus',
                              'Cardio-respiratoryfailureorcardio-respiratoryshock', 'Congestiveheartfailure',
                              'Acutecoronarysyndrome', 'Coronaryatherosclerosisoranginacerebrovasculardisease',
                              'Specifiedarrhythmias', 'OtherandUnspecifiedHeartDisease', 'Vascularorcirculatorydisease',
                              'Fibrosisoflungandotherchroniclungdisorders', 'Pneumonia', 'Historyofinfection',
                              'Metastaticcanceroracuteleukemia', 'LungUpperDigestiveTractandOtherSevereCancers',
                              'LymphaticHeadandNeckBrainandOtherMajorCancers;BreastColorectalandotherCancersandTumors;OtherRespiratoryandHeartNeoplasms',
                              'OtherDigestiveandUrinaryNeoplasms', 'Diabetesmellitus(DM)orDMcomplications',
                              'Protein-caloriemalnutrition', 'Disordersoffluidelectrolyteacid-base',
                              'OtherEndocrine/Metabolic/NutritionalDisorders', 'PancreaticDisease',
                              'PepticUlcerHemorrhageOtherSpecifiedGastrointestinalDisorders',
                              'OtherGastrointestinalDisorders', 'SevereHematologicalDisorders',
                              'Irondeficiencyorotheranemiasandblooddisease', 'Dementiaorotherspecifiedbraindisorders',
                              'Drug/AlcoholInducedDependence/Psychosis', 'MajorPsychiatricDisorders', 'Depression',
                              'AnxietyDisorders', 'OtherPsychiatricDisorders', 'QuadriplegiaParaplegiaParalysisFunctionalDisability',
                              'Polyneuropathy', 'HypertensiveHeartandRenalDiseaseorEncephalopathy'
                              ],
                     'HF': ['HistoryofCABG', 'Septicemia/shock', 'Congestiveheartfailure', 'Acutecoronarysyndrome',
                            'Coronaryatherosclerosisoranginacerebrovasculardisease', 'Valvularorrheumaticheartdisease',
                            'Specifiedarrhythmias', 'Vascularorcirculatorydisease', 'OtherandUnspecifiedHeartDisease',
                            'Metastaticcanceroracuteleukemia', 'Cancer', 'Diabetesmellitus(DM)orDMcomplications',
                            'Protein-caloriemalnutrition', 'Disordersoffluidelectrolyteacid-base',
                            'Liverandbiliarydisease', 'PepticUlcerHemorrhageOtherSpecifiedGastrointestinalDisorders',
                            'OtherGastrointestinalDisorders', 'SevereHematologicalDisorders',
                            'Irondeficiencyorotheranemiasandblooddisease', 'Dementiaorotherspecifiedbraindisorders',
                            'Drug/AlcoholInducedDependence/Psychosis', 'MajorPsychiatricDisorders', 'Depression',
                            'OtherPsychiatricDisorders', 'Hemiplegiaparaplegiaparalysisfunctionaldisability', 'Stroke',
                            'Chronicobstructivepulmonarydisease', 'Fibrosisoflungandotherchroniclungdisorders',
                            'Asthma', 'Pneumonia', 'End-stagerenaldiseaseordialysis', 'Renalfailure', 'Nephritis',
                            'Otherurinarytractdisorders', 'Decubitusulcerorchronicskinulcer'
                            ],
                     'HWR': ['Historyofinfection, Pneumonia', 'Metastaticcanceroracuteleukemia',
                             'LungUpperDigestiveTractandOtherSevereCancers',
                             'LymphaticHeadandNeckBrainandOtherMajorCancers;BreastColorectalandotherCancersandTumors;OtherRespiratoryandHeartNeoplasms',
                             'Diabetesmellitus(DM)orDMcomplications', 'Protein-caloriemalnutrition',
                             'End-stageliverdisease', 'Coagulationdefectsandotherspecifiedhematologicaldisorders',
                             'Drug/AlcoholInducedDependence/Psychosis, MajorPsychiatricDisorders',
                             'Hemiplegiaparaplegiaparalysisfunctionaldisability', 'Seizuredisordersandconvulsions',
                             'Chronicheartfailure', 'Coronaryatherosclerosisoranginacerebrovasculardisease',
                             'Specifiedarrhythmias', 'Chronicobstructivepulmonarydisease',
                             'Fibrosisoflungandotherchroniclungdisorders', 'Dialysisstatus',
                             'Decubitusulcerorchronicskinulcer', 'Septicemia/shock',
                             'Disordersoffluidelectrolyteacid-base', 'Irondeficiencyorotheranemiasandblooddisease',
                             'Renalfailure', 'PancreaticDisease', 'Rheumatoidarthritisandinflammatoryconnectivetissuedisease',
                             'Respiratordependence/tracheostomystatus', 'Transplants',
                             'Coagulationdefectsandotherspecifiedhematologicaldisorders', 'Hipfracture/dislocation'
                             ],
                     'PN': ['HistoryofCABG', 'Historyofinfection', 'Septicemia/shock', 'Metastaticcanceroracuteleukemia',
                            'LungUpperDigestiveTractandOtherSevereCancers',
                            'LymphaticHeadandNeckBrainandOtherMajorCancers;BreastColorectalandotherCancersandTumors;OtherRespiratoryandHeartNeoplasms',
                            'Diabetesmellitus(DM)orDMcomplications',
                            'Protein-caloriemalnutrition, Disordersoffluidelectrolyteacid-base',
                            'OtherGastrointestinalDisorders', 'SevereHematologicalDisorders',
                            'Irondeficiencyorotheranemiasandblooddisease', 'Dementiaorotherspecifiedbraindisorders',
                            'Drug/AlcoholInducedDependence/Psychosis', 'MajorPsychiatricDisorders',
                            'OtherPsychiatricDisorders', 'Hemiplegiaparaplegiaparalysisfunctionaldisability',
                            'Cardiorespiratoryfailureorcardio-respiratoryshock', 'Congestiveheartfailure',
                            'Acutecoronarysyndrome', 'Coronaryatherosclerosisoranginacerebrovasculardisease',
                            'Valvularorrheumaticheartdisease', 'Specifiedarrhythmias', 'Stroke',
                            'Vascularorcirculatorydisease', 'Chronicobstructivepulmonarydisease',
                            'Fibrosisoflungandotherchroniclungdisorders', 'Asthma', 'Pneumonia',
                            'Pleuraleffusion/pneumothorax', 'End-stagerenaldiseaseordialysis', 'Renalfailure',
                            'Urinarytractinfection', 'Otherurinarytractdisorders', 'Decubitusulcerorchronicskinulcer',
                            'VertebralFractures', 'Otherinjuries'
                            ],
                     'THA-TKA': ['Skeletaldeformities', 'Posttraumaticosteoarthritis', 'Morbidobesity',
                                 'Historyofinfection', 'Metastaticcanceroracuteleukemia', 'Cancer',
                                 'Diabetesmellitus(DM)orDMcomplications', 'Protein-caloriemalnutrition',
                                 'Disordersoffluidelectrolyteacid-base',
                                 'Rheumatoidarthritisandinflammatoryconnectivetissuedisease',
                                 'SevereHematologicalDisorders', 'Dementiaorotherspecifiedbraindisorders',
                                 'MajorPsychiatricDisorders', 'Hemiplegiaparaplegiaparalysisfunctionaldisability',
                                 'Polyneuropathy', 'Congestiveheartfailure', 'Coronaryatherosclerosis', 'Hypertension',
                                 'Specifiedarrhythmias', 'Stroke', 'Vascularorcirculatorydisease',
                                 'Chronicobstructivepulmonarydisease', 'Pneumonia', 'End-stagerenaldiseaseordialysis',
                                 'Renalfailure', 'Decubitusulcerorchronicskinulcer', 'CellulitisLocalSkinInfection',
                                 'Otherinjuries'
                                 ]
                     }

LACE_ATTRIBUTES = ['LengthofStay',  # LengthOfStay
                   'Inpatient_visits',  # EmergencyAdmission
                   # 'ComorbidityScore',
                   'ED_visits']  # ED_visits


def parse_user_input():
    """Validate and standardize user input to use as measure."""
    arg_parser = argparse.ArgumentParser(description="accepts name of measure to calculate score")
    arg_parser.add_argument("user_input",
                            type=str,
                            help="measure for which score is calculated: AMI, COPD, HF, HWR, PN, THA-TKA")
    args = arg_parser.parse_args()
    # user input MUST be a valid measure
    if args.user_input.upper() not in MEASURES:
        print("ERROR: Input must be a valid measure: AMI, COPD, HF, HWR, PN or THA-TKA.")
    else:
        return args.user_input.upper()


def get_comorbidity(row):
    """Sum all the instances of comorbid conditions."""
    comorbidity_score = 0
    try:
        # trim LACE columns from row
        comorbidity_score = row[3:].value_counts()['Yes']
    except KeyError:
        comorbidity_score = 0

    return comorbidity_score


def get_lace(data_col, val):
    """Calculate LACE score for specified column."""
    pass


def get_score(data_csv):
    """Calculate score for a health measure.
    :param data_csv - name of CSV file containing health data to parse
    """
    measure = parse_user_input()
    print("Getting score for %s..." % measure)

    # full data set from CSV
    full_df = pd.read_csv(data_csv,
                          index_col=0)
    # records for measure
    measure_df = full_df.loc[full_df['diagnosis_code'].isin(DIAGNOSIS_CODES[measure]),
                             LACE_ATTRIBUTES + COMORBIDITY_CODES[measure]]
    # calculation: comorbidity value for each row, in ComorbidityScore column
    measure_df['ComorbidityScore'] = measure_df.apply(get_comorbidity, axis=1)

    # calculation: lace score for each row as sum of points for each lace variable
    # (LengthOfStay, EmergencyAdmission, ComorbidityScore, EDVisit)
    print(measure_df)


if __name__ == '__main__':
    get_score('data/Sample Data 2016.csv')
