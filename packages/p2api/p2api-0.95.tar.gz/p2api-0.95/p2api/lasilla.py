import p2api

api = p2api.ApiConnection('production_lasilla', 'sam+MPGUtility', 'p2testing')

containerId = 2454628

api.createOB(containerId, 'TOM OB')