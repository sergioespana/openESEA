from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import time
import threading
import uuid

from ..DashboardRLModel import DashboardRLModel

INACTIVITY_THRESHOLD = 60 # 60 # 1 minute
INACTIVE_CHECK_INTERVAL = 20 # 10 seconds
modelInstances = {}

@method_decorator(csrf_exempt, name = 'dispatch')
@api_view(['POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny, ))
def dashboardsuggestions(request):
    print('Request Data', request.data)
    # return Response() # Temporarily disable rl backend
    global modelInstances

    modelInstanceId = request.data.get('modelInstanceId')
    dashboard = request.data.get('dashboard')
    ### Post dashboard model to (re-)build and run model ###
    if request.method == 'POST':
        # Get dashboard model from request
        if dashboard is None:
            return Response('No dashboard given!', status = status.HTTP_400_BAD_REQUEST)
        
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
            modelInstance.buildAndRunRLModel(dashboard)
            # Return succesful response
            return Response()
    
    ### Get recommendations ###
    elif request.method == 'PUT':
        # If there is no model instance yet, return error message
        if modelInstanceId is None or modelInstanceId not in modelInstances:
            return Response(f'Model instance with identifier {modelInstanceId} not found!', status = status.HTTP_404_NOT_FOUND)
        
        feedback = request.data.get('feedback')
        if feedback is not None:
            # For now print the feedback
            print(feedback)
            return Response()

        modelInstance = modelInstances[modelInstanceId]
    
        # Get actions and return it
        actions = modelInstance.retrieveBestActions()
        return Response(actions)
    
    ### Delete model when unloading dashboard ###
    elif request.method == 'DELETE':
        # If there is no model instance yet, return error message
        if modelInstanceId not in modelInstances:
            return Response(f'Model instance with identifier {modelInstanceId} not found!', status = status.HTTP_404_NOT_FOUND)
        
        modelInstance = modelInstances[modelInstanceId]
        print('Terminating model with modelInstanceId: ', modelInstanceId)
        modelInstance.terminate()
        del modelInstances[modelInstanceId]
        
        return Response('Model deleted!')
    else:
        return Response('')

class DashboardRLModelInstance():
    def __init__(self, dashboard):
        self.thread = None
        self.buildAndRunRLModel(dashboard)

    def buildAndRunRLModel(self, dashboard):
        self.updateLastActivity()

        # Terminate existing thread
        if self.thread is not None: self.terminate(wait = True)

        # Exit if dashboard is empty
        self.dashboard = dashboard
        if self.dashboard == []: 
            self.model = None
            return

        self.buildRLModel()
        self.runRLModel()

    # def rebuildAndRunRLModel(self, dashboard):
    #     self.updateLastActivity()

    #     self.terminate(wait = True) # Stop previous model and Wait until last episode is done
    #     self.buildAndRunRLModel(dashboard) # Override previous model and run model
        
    def buildRLModel(self):
        # Build RL model
        self.model = DashboardRLModel.DashboardRLModel(self.dashboard)
        print('Model is built!')

    def runRLModel(self):
        # Start running model in separate thread
        self.thread = threading.Thread(target = self.model.run)
        self.thread.daemon = True
        self.thread.start()
        print('Running model...')

    def retrieveBestActions(self):
        if self.model is None: return []

        self.updateLastActivity()

        # Predict best action from model and return this in response
        return self.model.best_actions
    
    def updateLastActivity(self):
        self.lastActivity = time.time()

    def terminate(self, wait = False):
        # Terminate model after last episode is done
        if self.model is not None: self.model.kill()
        # Wait for episode to finish
        if wait and self.thread is not None: self.thread.join()

# Keep track of active model instances, and terminate instances which have been inactive for some time
def stopInactiveModelInstances():
    while True:
        currentTime = time.time()
        # Identify inactive model instances
        inactiveModelInstanceIds = []
        for modelInstanceId in modelInstances:
            modelInstance = modelInstances[modelInstanceId]
            if currentTime - modelInstance.lastActivity > INACTIVITY_THRESHOLD:
                inactiveModelInstanceIds.append(modelInstanceId)
        # Delete from dict of active models
        for inactiveModelInstanceId in inactiveModelInstanceIds:
            modelInstance = modelInstances[inactiveModelInstanceId]
            print('Terminating model with modelInstanceId: ', modelInstanceId)
            modelInstance.terminate()
            del modelInstances[inactiveModelInstanceId]

        # Sleep for a while before checking again (e.g., every minute)
        time.sleep(INACTIVE_CHECK_INTERVAL)

# Start the function to periodically check for inactive model instances as a separate thread
stopInactiveModelsThread = threading.Thread(target = stopInactiveModelInstances)
stopInactiveModelsThread.daemon = True  # Make the thread a daemon, so it terminates when the main program exits
stopInactiveModelsThread.start()
