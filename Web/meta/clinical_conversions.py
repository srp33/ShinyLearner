#http://www.cancer.org/treatment/understandingyourdiagnosis/staging
#this is the proposed numerization for non-continuous variables
#survival thresholds are also set forth below
to_numerize = {}
to_numerize['blca'] = {
	'pstage':{'Stage III': 1, 'Stage II': 0, 'Stage I': 0, 'Stage IV': 2},\
	'subtype_blca':{'Papillary': 1, 'Non-Papillary': 0},\
	'pstage_n':{'N0': 0, 'N1': 1, 'N2': 2, 'N3': 2, 'NX': np.nan},\
	'grade':{'Low Grade': 0, 'High Grade': 1},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'other_dx':{'Yes': 1, 'No': 0},\
	'smoking':{1.0: 0, 2.0: 1, 3.0: 2, 4.0: 3, 5.0: 4},\
	'race_ethn':{'WHITE':0, 'BLACK OR AFRICAN AMERICAN':1, 'ASIAN':2, 'HISPANIC OR LATINO':3},\
	'pstage_t':{'TX': np.nan, 'T2a': 1, 'T3b': 2, 'T4': 3, 'T2b': 1, 'T2': 1, 'T3': 2, 'T0': 0, 'T3a': 2, 'T4b': 3, 'T4a': 3, 'T1': 0}\
}
to_numerize['brca'] = {
	'pstage':{'Stage IA': 0, 'Stage III': 2, 'Stage IB': 0, 'Stage I': 0, 'Stage IIA': 1, 'Stage IIB': 1, 'Stage IIIA': 2, 'Stage II': 1, 'Stage IIIC': 2, 'Stage IIIB': 2, 'Stage X': np.nan, 'Stage IV': 3},\
	'pstage_n':{'NX': np.nan, 'N0 (mol+)': np.nan, 'N3a': 3, 'N2a': 2, 'N3c': 3, 'N0 (i-)': 0, 'N1b': 1, 'N1c': 1, 'N1a': 1, 'N1mi': 1, 'N0': 0, 'N1': 1, 'N2': 2, 'N3': 3, 'N0 (i+)': 0, 'N3b': 3},\
	'estr_r':{'Positive': 1, 'Indeterminate': np.nan, 'Negative': 0},\
	'subtype':{'Other, specify': 0, 'Infiltrating Ductal Carcinoma': 1, 'Infiltrating Carcinoma NOS': 1, 'Metaplastic Carcinoma': 2, 'Mucinous Carcinoma': 3, 'Mixed Histology (please specify)': 0, 'Medullary Carcinoma': 4, 'Infiltrating Lobular Carcinoma': 5},\
	'race':{'WHITE': 0, 'BLACK OR AFRICAN AMERICAN': 1, 'ASIAN': 2, 'AMERICAN INDIAN OR ALASKA NATIVE': 3},\
	'prog_r':{'Positive': 1, 'Indeterminate': np.nan, 'Negative': 0},\
	'menopause':{'Pre (<6 months since LMP AND no prior bilateral ovariectomy AND not on estrogen replacement)': 0, 'Peri (6-12 months since last menstrual period)': 1, 'Post (prior bilateral ovariectomy OR >12 mo since LMP with no prior hysterectomy)': 1, 'Indeterminate (neither Pre or Postmenopausal)': np.nan},\
	'other_dx':{'Yes': 1, 'No': 0},\
	'pstage_t':{'T1a': 0, 'TX': np.nan, 'T1b': 0, 'T1c': 0, 'T2a': 1, 'T4': 3, 'T2b': 1, 'T2': 1, 'T3': 2, 'T1': 0, 'T4b': 3, 'T3a': 2, 'T4d': 3}
}
to_numerize['gbm'] = {
	'race_ethn':{'BLACK OR AFRICAN AMERICAN':0, 'AMERICAN INDIAN OR ALASKA NATIVE':1, 'ASIAN':2, 'HISPANIC OR LATINO':3, 'WHITE':4},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'subtype':{'Glioblastoma Multiforme (GBM)': 0, 'Untreated primary (de novo) GBM': 1, 'Treated primary GBM': 2},\
	'race':{'WHITE': 0, 'BLACK OR AFRICAN AMERICAN': 1, 'ASIAN': 2},\
	'hx_lgg':{'YES': 1, 'NO': 0},\
	'neoadj':{'Yes': 1, 'No': 0}
}
to_numerize['hnsc'] = {
	'race_ethn':{'BLACK OR AFRICAN AMERICAN':0, 'AMERICAN INDIAN OR ALASKA NATIVE':1, 'ASIAN':2, 'HISPANIC OR LATINO':3, 'WHITE':4},\
	'subdiv':{'Buccal Mucosa': 0, 'Hypopharynx': 1, 'Tonsil': 2, 'Hard Palate': 3, 'Oral Tongue': 4, 'Larynx': 5, 'Oropharynx':6, 'Floor of mouth': 7, 'Alveolar Ridge': 8, 'Lip': 9, 'Base of tongue': 10, 'Oral Cavity': 11},\
	'grade':{'G4': 2, 'G3': 2, 'G2': 1, 'G1': 0, 'GX': np.nan},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'alcohol':{'YES': 1, 'NO': 0},\
	'cstage_t':{'TX': np.nan, 'T4': 3, 'T2': 1, 'T3': 2, 'T1': 0, 'T4b': 3, 'T4a': 3},\
	'other_dx':{'Yes, History of Synchronous/Bilateral Malignancy': 1, 'Yes': 1, 'Yes, History of Prior Malignancy': 1, 'No': 0},\
	'smoking':{1.0: 0, 2.0: 1, 3.0: 2, 4.0: 3, 5.0: 3},\
	'neoadj':{'Yes': 1, 'No': 0},\
	'cstage_n':{'N2c': 2, 'N2b': 2, 'N2a': 2, 'NX': np.nan, 'N0': 0, 'N1': 1, 'N2': 2, 'N3': 2},\
	'cstage':{'Stage III': 1, 'Stage I': 0, 'Stage II': 0, 'Stage IVA': 2, 'Stage IVB': 2, 'Stage IVC': 2},\
	'pstage_t':{'TX': np.nan, 'T4': 3, 'T2': 1, 'T3': 2, 'T0': 0, 'T1': 0, 'T4b': 3, 'T4a': 3}
}
to_numerize['kirc'] = {
	'pstage':{'Stage III': 2, 'Stage II': 1, 'Stage I': 0, 'Stage IV': 3},\
	'pstage_m':{'M1': 1, 'M0': 0, 'MX': np.nan},\
	'grade':{'G4': 2, 'G3': 1, 'G2': 0, 'G1': 0, 'GX': np.nan},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'lateral':{'Right': 0, 'Bilateral': 1, 'Left': 2},\
	'race':{'WHITE': 0, 'BLACK OR AFRICAN AMERICAN': 1, 'ASIAN': 2},\
	'other_dx':{'Yes, History of Synchronous/Bilateral Malignancy': 1, 'Yes': 1, 'Yes, History of Prior Malignancy': 1, 'No': 0},\
	'pstage_t':{'T1a': 0, 'T1b': 0, 'T2a': 1, 'T2': 1, 'T4': 3, 'T2b': 1, 'T3b': 2, 'T3': 2, 'T1': 0, 'T3c': 2, 'T3a': 2}
}
to_numerize['laml'] = {
	'race_ethn':{'WHITE':0, 'BLACK OR AFRICAN AMERICAN':1, 'ASIAN':2, 'HISPANIC OR LATINO':3},\
	'neoadj_hu':{'YES': 1, 'NO': 0},\
	'neoadj':{'Yes': 1, 'No': 0},\
	'atra':{'YES': 1, 'NO': 0},\
	'fab_code':{'Not Classified': np.nan, 'M5': 5, 'M4': 4, 'M7': 5, 'M6': 5, 'M1': 1, 'M3': 3, 'M2': 2, 'M0 Undifferentiated': 0},\
	'cyto_risk':{'Poor': 2, 'Intermediate/Normal': 1, 'Favorable': 0},\
	'other_dx':{'Yes': 1, 'No': 0},\
	'gender':{'MALE': 0, 'FEMALE': 1}
}
to_numerize['lgg'] = {
	'race_ethn':{'BLACK OR AFRICAN AMERICAN':0, 'AMERICAN INDIAN OR ALASKA NATIVE':1, 'ASIAN':2, 'HISPANIC OR LATINO':3, 'WHITE':4},\
	'subtype':{'Oligoastrocytoma': 0, 'Oligodendroglioma': 1, 'Astrocytoma': 2},\
	'grade':{'G3': 1, 'G2': 0},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'lateral':{'Right': 1, 'Midline': 0, 'Left': 2},\
	'site':{'Supratentorial, Temporal Lobe': 0, 'Supratentorial, Frontal Lobe': 1, 'Posterior Fossa, Cerebellum': 2, 'Supratentorial, Not Otherwise Specified': np.nan, 'Supratentorial, Parietal Lobe': 3, 'Posterior Fossa, Brain Stem': 4, 'Supratentorial, Occipital Lobe': 5},\
	'hx_head':{'YES': 1, 'NO': 0},\
	'hx_seiz':{'YES': 1, 'NO': 0},\
	'other_dx':{'Yes, History of Synchronous/Bilateral Malignancy': 1, 'Yes': 1, 'Yes, History of Prior Malignancy': 1, 'No': 0},\
	'neoadj':{'Yes, Radiation Prior to Resection': 1, 'Yes': 1, 'Yes, Pharmaceutical Treatment Prior to Resection': 1, 'No': 0}
}
to_numerize['lihc'] = {
	'race_ethn':{'BLACK OR AFRICAN AMERICAN':0, 'AMERICAN INDIAN OR ALASKA NATIVE':1, 'ASIAN':2, 'HISPANIC OR LATINO':3, 'WHITE':4},\
	'pstage':{'Stage III': 2, 'Stage I': 0, 'Stage II': 1, 'Stage IIIA': 2, 'Stage IIIC': 2, 'Stage IIIB': 2, 'Stage IVA': 3, 'Stage IVB': 3, 'Stage IV': 3},\
	'grade':{'G4': 2, 'G3': 2, 'G2': 1, 'G1': 0},\
	'other_dx':{'Yes': 1, 'No': 0},\
	'gender':{'MALE': 1, 'FEMALE': 0},\
	'pstage_t':{'TX': np.nan, 'T2a': 1, 'T2': 1, 'T4': 3, 'T2b': 1, 'T3b': 2, 'T3': 2, 'T0': 0, 'T3a': 2, 'T1': 0}
}
to_numerize['luad'] = {
	'pstage_n':{'N0': 0, 'N1': 1, 'N2': 2, 'N3': 2, 'NX': np.nan},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'pstage':{'Stage IA': 0, 'Stage IB': 0, 'Stage I': 0, 'Stage IIA': 1, 'Stage IIB': 1, 'Stage IIIA': 2, 'Stage II': 1, 'Stage IIIB': 2, 'Stage IV': 3},\
	'subdiv':{'L-Upper': 0, 'R-Upper': 1, 'L-Lower': 2, 'Other (please specify)': np.nan, 'Bronchial': 5, 'R-Middle': 3, 'R-Lower': 4},\
	'smoking':{1.0: 0, 2.0: 1, 3.0: 2, 4.0: 3, 5.0: 3},\
	'pstage_t':{'T1a': 0, 'T1b': 0, 'T2a': 1, 'T4': 2, 'T2b': 1, 'T2': 1, 'T3': 2, 'T1': 0, 'TX': np.nan}
}
to_numerize['lusc'] = {
	'pstage_n':{'N0': 0, 'N1': 1, 'N2': 2, 'N3': 2, 'NX': np.nan},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'pstage':{'Stage IA': 0, 'Stage III': 2, 'Stage IB': 0, 'Stage I': 0, 'Stage IIA': 1, 'Stage IIB': 1, 'Stage IIIA': 2, 'Stage II': 1, 'Stage IIIB': 2, 'Stage IV': 2},\
	'subdiv':{'L-Upper': 0, 'R-Upper': 1, 'L-Lower': 2, 'Other (please specify)': np.nan, 'Bronchial': 3, 'R-Middle': 4, 'R-Lower': 5},\
	'other_dx':{'Yes, History of Synchronous/Bilateral Malignancy': 1, 'Yes': 1, 'Yes, History of Prior Malignancy': 1, 'No': 0},\
	'pstage_t':{'T1a': 0, 'T1b': 0, 'T2a':1, 'T4': 3, 'T2b': 1, 'T2': 1, 'T3': 2, 'T1': 0}
}
to_numerize['ov'] = {
	'grade':{'G4': 1, 'G3': 1, 'G2': 0, 'G1': 0, 'GX': np.nan, 'GB': np.nan},\
	'subdiv':{'Right': 0, 'Bilateral': 1, 'Left': 2},\
	'race':{'NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER': 0, 'WHITE': 1, 'BLACK OR AFRICAN AMERICAN': 2, 'ASIAN': 3, 'AMERICAN INDIAN OR ALASKA NATIVE': 4},\
	'cstage':{'Stage IA': 0, 'Stage IC': 0, 'Stage IB': 0, 'Stage IIA': 1, 'Stage IIC': 1, 'Stage IIB': 1, 'Stage IIIA': 2, 'Stage IIIC': 2, 'Stage IIIB': 2, 'Stage IV': 3}
}
to_numerize['sarc'] = {
	'multifocal':{'YES': 1, 'NO': 0},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'subtype':{'Desmoid Tumor':0, "Pleomorphic 'MFH' / Undifferentiated pleomorphic sarcoma": 1, "Giant cell 'MFH' / Undifferentiated pleomorphic sarcoma with giant cells": 2, 'Synovial Sarcoma - Biphasic': 3, 'Leiomyosarcoma (LMS)': 4, 'Sarcoma; synovial; poorly differentiated': 5, 'Myxofibrosarcoma': 6, 'Malignant Peripheral Nerve Sheath Tumors (MPNST)': 7, 'Undifferentiated Pleomorphic Sarcoma (UPS)': 1, 'Synovial Sarcoma - Monophasic': 8, 'Dedifferentiated liposarcoma': 9},\
	'race':{'WHITE': 0, 'BLACK OR AFRICAN AMERICAN': 1, 'ASIAN': 2},\
	'other_dx':{'Yes': 1, 'No': 0}
}
to_numerize['skcm'] = {
	'race_ethn':{'WHITE':0, 'BLACK OR AFRICAN AMERICAN':1, 'ASIAN':2, 'HISPANIC OR LATINO':3},\
	'pstage':{'Stage III': 2, 'Stage IA': 0, 'Stage IB': 0, 'Stage I': 0, 'Stage II': 1, 'Stage IIC': 1, 'Stage IIB': 1, 'Stage IIIA': 2, 'Stage IIA': 1, 'Stage IIIC': 2, 'Stage IIIB': 2, 'Stage IV': 3, 'Stage 0': 0, 'I/II NOS': np.nan},\
	'pstage_n':{'NX': np.nan, 'N2c': 2, 'N2b': 2, 'N2a': 2, 'N1b': 1, 'N1a': 1, 'N0': 0, 'N1': 1, 'N2': 2, 'N3': 3},\
	'pstage_m':{'M1a': 1, 'M1c': 1, 'M1b': 1, 'M1': 1, 'M0': 0},\
	'site_skcm':{'Trunk|[Not Available]': np.nan, 'Extremities|Trunk': 0, 'Other  Specify': np.nan, 'Head and Neck': 1, 'Trunk': 2, 'Extremities': 3, 'Trunk|Extremities': 4, 'Extremities|Extremities': 5},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'prim_melanoma':{'YES': 1, 'NO': 0},\
	'other_dx':{'Yes': 1, 'No': 0},\
	'relapse':{'YES': 1, 'NO': 0},\
	'pstage_t':{'T1b': 1, 'T1a': 1, 'TX': np.nan, 'T2a': 2, 'T3b': 3, 'T4': 4, 'T2b': 2, 'T2': 2, 'T3': 3, 'T0': 0, 'T3a': 3, 'Tis': np.nan, 'T4b': 4, 'T4a': 4, 'T1': 1},\
	'neoadj':{'Yes': 1, 'No': 0}
}
to_numerize['stad'] = {
	'pstage_n':{'N3a': 3, 'N3b': 3, 'NX': np.nan, 'N0': 0, 'N1': 1, 'N2': 2, 'N3': 3},\
	'pstage_m':{'M1': 1, 'M0': 0, 'MX': np.nan},\
	'grade':{'G3': 1, 'G2': 0, 'G1': 0, 'GX': np.nan},\
	'gender':{'MALE': 0, 'FEMALE': 1},\
	'pstage':{'Stage IA': 0, 'Stage III': 2, 'Stage IB': 0, 'Stage I': 0, 'Stage IIA': 1, 'Stage IIB': 1, 'Stage IIIA': 2, 'Stage II': 1, 'Stage IIIC': 2, 'Stage IIIB': 2, 'Stage IV': 3},\
	'subdiv':{'Stomach (NOS)': np.nan, 'Fundus/Body': 0, 'Other (please specify)': np.nan, 'Gastroesophageal Junction': 1, 'Cardia/Proximal': 2, 'Antrum/Distal': 3},\
	'other_dx':{'Yes': 1, 'Yes, History of Prior Malignancy': 1, 'No': 0},\
	'pstage_t':{'TX': np.nan, 'T1b': 0, 'T2a': 1, 'T4': 3, 'T2b': 1, 'T2': 1, 'T3': 2, 'T1': 0, 'T4b': 3, 'T4a': 3, 'T1a': 0}
}
half = 183 #days
thresholds = {'blca':half*4, 'brca':half*13, 'gbm':half*2, 'hnsc':half*4, 'kirc':half*8, 'laml':half*2,'lgg':half*8, 'lihc':half*6, 'luad':half*5, 'lusc':half*5, 'ov':half*6, 'sarc':half*6,'skcm':half*11, 'stad':half*3}