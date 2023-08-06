#!/usr/bin/env python
# encoding: utf-8

NO_ST_COLUMNS = {
    "term": "Trimestre",
    "assessment": "Nom",
    "date": "Date",
    "exercise": "Exercice",
    "question": "Question",
    "competence": "Competence",
    "theme": "Domaine",
    "comment": "Commentaire",
    "score_rate": "Bareme",
    "is_leveled": "Est_nivele",
}

COLUMNS = {
    **NO_ST_COLUMNS,
    "student": "Eleve",
    "score": "Score",
    "mark": "Note",
    "level": "Niveau",
    "normalized": "Normalise",
}

VALIDSCORE = {
    "NOTFILLED": "",  # The item is not scored yet
    "NOANSWER": ".",  # Student gives no answer (this score will impact the fianl mark)
    "ABS": "a",  # Student has absent (this score won't be impact the final mark)
}
