algorithm = "TOFL"


legends_dicts = { "en": {"random": "Random",
                         "m_fastest": "M-Fastest (M=50%)",
                         "tofl_oracle": algorithm+" Oracle",
                         "tofl_estimator_dl" : algorithm+" Estimator",
                         "tofl": algorithm+" Estimator",
                         "tofl_estimator_m_fastest": algorithm+" with M-Fastest",
                         "tofl_estimator_m_fastest_clients": algorithm+" with M-Fastest",
                         "tofl_mfastest": algorithm+" with M-Fastest"},

                "pt":   {"random": "Aleatório",
                         "m_fastest": "M-Fastest (M=50%)",
                         "tofl_oracle": algorithm+" Oráculo",
                         "tofl_estimator_dl" : algorithm+" Estimador",
                         "tofl": algorithm+" Estimador",
                         "tofl_estimator_m_fastest": algorithm+" com M-Fastest",
                         "tofl_estimator_m_fastest_clients": algorithm+" com M-Fastest",
                         "tofl_mfastest": algorithm+" com M-Fastest"} 
                         
                         }

style = {"random": "-",
         "m_fastest": "--",
         "tofl_oracle": "-.",
         "tofl": "-",
         "tofl_estimator_dl": "-",
         "tofl_estimator_m_fastest": (0, (1, 3)),
         "tofl_estimator_m_fastest_clients": (0, (1, 3)),
         "tofl_mfastest":(0, (3, 10, 1, 10))}

colors = {"random": "b",
          "m_fastest": "r",
          "tofl_oracle": "y",
          "tofl": "k",
          "tofl_estimator_dl": "k",
          "tofl_estimator_m_fastest": "g",
          "tofl_estimator_m_fastest_clients": "g",
          "tofl_mfastest":"gray"}
