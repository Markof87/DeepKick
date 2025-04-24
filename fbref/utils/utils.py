from collections import defaultdict

def parse_tuple_key(key):
    # Rimuove parentesi e spazi, poi splitta per virgola
    key = key.strip()
    if key.startswith("(") and key.endswith(")"):
        key = key[1:-1]
    parts = [p.strip().strip("'") for p in key.split(",")]
    # Rimuove eventuali stringhe vuote alla fine
    if parts and parts[-1] == '':
        parts = parts[:-1]
    return parts

def parse_team_key(key):
    # Estrae il nome squadra dall'ultima posizione della tupla
    key = key.strip()
    if key.startswith("(") and key.endswith(")"):
        key = key[1:-1]
    parts = [p.strip().strip("'") for p in key.split(",")]
    return parts[-1]

def restructure_json(data):
    out = {}
    nested = defaultdict(dict)

    for k, v in data.items():
        main_parts = parse_tuple_key(k)
        if len(main_parts) == 1:
            # Caso semplice: "('players_used', '')"
            metric = main_parts[0]
            metric_dict = {}
            for team_k, value in v.items():
                team = parse_team_key(team_k)
                metric_dict[team] = value
            out[metric] = metric_dict
        elif len(main_parts) == 2:
            # Caso annidato: "('Playing Time', 'MP')"
            group, metric = main_parts
            metric_dict = {}
            for team_k, value in v.items():
                team = parse_team_key(team_k)
                metric_dict[team] = value
            nested[group][metric] = metric_dict
        else:
            # Caso imprevisto, fallback
            out[k] = v

    # Unisci i gruppi annidati
    for group, metrics in nested.items():
        out[group] = metrics

    return out

