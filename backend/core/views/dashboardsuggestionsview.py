from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import threading
import uuid

from ..DashboardRLModel import DashboardRLModel

modelInstances = {}

# modelInstance verwijderen uit deze mapping als model inactive is!!!!!!
# modelInstanceId meegeven aan requests, met modelInstanceId = request.data['modelInstanceId]
# dashboard meegeven aan requests, zodat dashboard = request.data['dashboard'] ipv request.data

@method_decorator(csrf_exempt, name = 'dispatch')
@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny, ))
def dashboardsuggestions(request):
    print('Request Data', request.data)
    return Response() # Temporarily disable rl backend

    modelInstanceId = request.data.get('modelInstanceId')
    dashboard = request.data.get('dashboard')
    ### Post dashboard model to (re-)build and run model ###
    if request.method == 'POST':
        # Get dashboard model from request
        if dashboard is None:
            return Response('No dashboard given!')
        
        # If there is no model instance yet, create a new one from dashboard
        if modelInstanceId is None:
            # Generate a unique identifier
            modelInstanceId = str(uuid.uuid4())
            # Initialize instance from dashboard to build & run model
            modelInstance = DashboardRLModelInstance(dashboard)
            modelInstances[modelInstanceId] = modelInstance
            # Return succesful response with the generated modelInstanceId
            return Response({ 'modelInstanceId': modelInstanceId })
        else: 
            # Rebuild model from dashboard & run model
            modelInstance = modelInstances[modelInstanceId]
            modelInstance.rebuildAndRunRLModel(dashboard)
            # Return succesful response
            return Response()
    
    ### Delete model when unloading dashboard ###
    elif request.method == 'DELETE':
        # If there is no model instance yet, return error message
        if modelInstanceId not in modelInstances:
            return Response(f'Model instance with identifier {modelInstanceId} not found!')
        
        modelInstance = modelInstances[modelInstanceId]

        modelInstance.terminate()
        return Response('Model deleted!')
    
    ### Get recommendations ###
    elif request.method == 'PUT':
        # If there is no model instance yet, return error message
        if modelInstanceId is None or modelInstanceId not in modelInstances:
            return Response(f'Model instance with identifier {modelInstanceId} not found!')
        
        modelInstance = modelInstances[modelInstanceId]
    
        # Get actions and return it
        actions = modelInstance.retrieveBestActions()
        return Response({ 'request': '', 'actions': actions.to_dict() })
    else:
        return Response()

class DashboardRLModelInstance():
    def __init__(self, dashboard):
        self.buildAndRunRLModel(dashboard)

    def buildAndRunRLModel(self, dashboard):
        self.buildRLModel(dashboard)
        self.runRLModel()

    def rebuildAndRunRLModel(self, dashboard):
        self.terminate(wait = True) # Stop previous model and Wait until last episode is done
        self.buildAndRunRLModel(dashboard) # Override previous model and run model
        
    def buildRLModel(self, dashboard):
        # Build RL model
        self.model = DashboardRLModel.DashboardRLModel(dashboard)
        print('Model is built!')

    def runRLModel(self):
        # Start running model in separate thread
        self.thread = threading.Thread(target = self.model.run)
        self.thread.start()
        print('Running model...')

    def retrieveBestActions(self):
        # Otherwise, predict best action from model and return this in response
        action = self.model.predict()
        return action
    
    def terminate(self, wait = False):
        # Terminate model after last episode is done
        self.model.kill()
        # Wait for episode to finish
        if wait: self.thread.join()
