from dlanalytics import Analytics
import numpy as np

analytics = Analytics(host='localhost', port=8000)

# analytics.latest_project_id = 1
proj, is_new = analytics.create_project('Senet 18', 'A siamese model')

trial = analytics.create_trial(name='trial 1', params={'module': 'resnet', 'data': np.arange(100)})

analytics.update_trial(trial_id=trial.id, results={'acc': 1.0} )

trial = analytics.create_trial(name='trial 1', params={'module': 'resnet'} )

analytics.update_trial(trial_id=trial.id, results={'acc': 1.0} )

print(analytics.project())