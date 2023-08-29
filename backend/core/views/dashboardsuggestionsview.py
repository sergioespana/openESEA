from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import threading

from ..DashboardRLModel import DashboardRLModel

modelInstance = None

@method_decorator(csrf_exempt, name = 'dispatch')
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes((AllowAny, ))
def dashboardsuggestions(request):
    global modelInstance

    ### Post dashboard model to build and run model ###
    if request.method == 'POST':
        dashboard = request.data

        # Initialize Instance for Model and build & run model
        modelInstance = DashboardRLModelInstance(dashboard)

        # Return succesful response
        return Response()
    
    ### Rebuild dashboard model from updated dashboard ###
    elif request.method == 'PUT':
        # If there is no model instance yet, return error message
        if modelInstance is None:
            return Response('No model built yet!')
        
        dashboard = request.data

        # Initialize Instance for Model and build & run model
        modelInstance.rebuildModel(dashboard)

        # Return succesful response
        return Response()
    
    ### Get recommended action from trained model ###
    elif request.method == 'GET':
        # If there is no model instance yet, return error message
        if modelInstance is None:
            return Response('No model built yet!')
        
        # Otherwise get action and return it
        action = modelInstance.getAction()
        return Response({ 'request': '', 'action': action.to_dict() })
    
    ### Delete model when unloading dashboard ###
    elif request.method == 'DELETE':
        modelInstance.terminate()
        return Response('Model deleted!')
    else:
        return Response()

class DashboardRLModelInstance():
    def __init__(self, dashboard):
        self.initializeRLModel(dashboard)

    def initializeRLModel(self, dashboard):
        self.buildModelFromDashboard(dashboard)
        self.runModel()
        
    def buildModelFromDashboard(self, dashboard):
        # Build RL model
        self.model = DashboardRLModel.DashboardRLModel(dashboard)
        print('Model is built!')

    def rebuildModel(self, dashboard):
        self.terminate(wait = True) # Wait until last episode is done
        self.initializeRLModel(dashboard)

    def runModel(self):
        # Start running model in separate thread
        self.thread = threading.Thread(target = self.model.run)
        self.thread.start()
        print('Running model...')

    def getAction(self):
        # Otherwise, predict best action from model and return this in response
        action = self.model.predict()
        return action
    
    def terminate(self, wait = False):
        # Terminate model after last episode is done
        self.model.kill()
        # Wait for episode to finish
        if wait: self.thread.join()
