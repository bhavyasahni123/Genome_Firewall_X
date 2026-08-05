from pprint import pprint

from .aggregator import ResultAggregator


predictions = {

    "ampicillin": {

        "prediction": "Resistant",

        "probability": 0.94,

    },

    "cefotaxime": {

        "prediction": "Susceptible",

        "probability": 0.21,

    },

    "ciprofloxacin": {

        "prediction": "Resistant",

        "probability": 0.88,

    },

    "gentamicin": {

        "prediction": "Susceptible",

        "probability": 0.11,

    },

    "meropenem": {

        "prediction": "Susceptible",

        "probability": 0.03,

    },

}

feature_summary = {

    "Total_AMR_Hits": 17,

    "Unique_AMR_Genes": 12,

    "Unique_Classes": 6,

    "Unique_Subclasses": 8,

    "Unique_Types": 2,

    "Unique_Methods": 4,

}

aggregator = ResultAggregator()

result = aggregator.aggregate(

    genome_id="562.65207",

    predictions=predictions,

    feature_summary=feature_summary,

)

pprint(result)