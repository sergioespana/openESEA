def getVisualisations(requestData):
    # Get dashboard model from request data
    dashboardModel = requestData['dashboard']
    if dashboardModel is None:
        return None
    
    # Determine selected overview
    selectionConfig = requestData['config']
    if selectionConfig:
        currentOverviewIndex = selectionConfig['overviewId']
    if currentOverviewIndex is None:
        currentOverviewIndex = 0

    overviews = dashboardModel['Overviews']
    if overviews is None: return None 
    currentOverview = overviews[currentOverviewIndex]
    if currentOverview is None: return None

    bodysection = currentOverview['BodySection']
    if bodysection is None: return None
    containers = bodysection['Containers']
    if containers is None: return None

    visualisationsList = []
    for container in containers:
        visualisationConfigs = container['Visualisations']
        if visualisationConfigs is None: continue
        for visualisationConfig in visualisationConfigs:
            visualisation = {}
            dataDisplay = visualisation['DataDisplay']
            if dataDisplay is None: continue
            visualisation['Visualisation Type'] = dataDisplay['Type']
            visualisation['Other Info'] = dataDisplay['DataConfiguration']
            visualisationsList.append(visualisation)
    
    dashboardData = requestData['data']
    return []