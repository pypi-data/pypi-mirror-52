from edc_constants.constants import FEMALE, MALE
from edc_reportable import site_reportables, parse as p, adult_age_options
from edc_reportable import MILLIGRAMS_PER_DECILITER, MILLIMOLES_PER_LITER
from edc_reportable import MICROMOLES_PER_LITER, IU_LITER
from edc_reportable import GRAMS_PER_DECILITER, TEN_X_9_PER_LITER
from edc_reportable.grading_data.daids_july_2017 import hematology, chemistries

normal_data = {
    "glucose": [],
    "hematocrit": [],
    "rbc": [],
    "hba1c": [],
    "eGFR": [],
    "ast": [],
    "alp": [],
    "serum amylase": [],
    "ggt": [],
    "serum albumin": [],
    "serum urea": [],
    "serum uric acid": [],

    "haemoglobin": [
        p("13.5<=x<=17.5", units=GRAMS_PER_DECILITER,
          gender=[MALE], **adult_age_options),
        p("12.0<=x<=15.5", units=GRAMS_PER_DECILITER,
          gender=[FEMALE], **adult_age_options),
    ],
    "platelets": [
        p("150<=x<=450", units=TEN_X_9_PER_LITER,
          gender=[MALE, FEMALE], **adult_age_options)
    ],
    "neutrophil": [
        p("2.5<=x<=7.5", units=TEN_X_9_PER_LITER,
          gender=[MALE, FEMALE], **adult_age_options)
    ],
    "sodium": [
        p("135<=x<=145", units=MILLIMOLES_PER_LITER,
          gender=[MALE, FEMALE], **adult_age_options)
    ],
    "potassium": [
        p("3.6<=x<=5.2", units=MILLIMOLES_PER_LITER,
          gender=[MALE, FEMALE], **adult_age_options)
    ],
    "magnesium": [
        p(
            "0.75<=x<=1.2",
            units=MILLIMOLES_PER_LITER,
            gender=[MALE, FEMALE],
            **adult_age_options,
        ),
        p(
            "1.8<=x<=2.9",
            units=MILLIGRAMS_PER_DECILITER,
            gender=[MALE, FEMALE],
            **adult_age_options,
        ),
    ],
    "alt": [p("10<=x<=40", units=IU_LITER, gender=[MALE, FEMALE], **adult_age_options)],
    "creatinine": [
        p(
            "0.6<=x<=1.3",
            units=MILLIGRAMS_PER_DECILITER,
            gender=[MALE, FEMALE],
            **adult_age_options,
        ),
        p("53<=x<=115", units=MICROMOLES_PER_LITER,
          gender=[MALE, FEMALE], **adult_age_options),
    ],
    "wbc": [p("2.49<x", units=TEN_X_9_PER_LITER, gender=[MALE, FEMALE], **adult_age_options)],
}

grading_data = {}
grading_data.update(**chemistries)
grading_data.update(**hematology)

site_reportables.register(
    name="meta", normal_data=normal_data, grading_data=grading_data
)
