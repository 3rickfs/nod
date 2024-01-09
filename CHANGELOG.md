# Change Log

## [1.0.3] 2024-01-08
### Add
- Second test in test_nod_distribution_and_operation.py running ok, distributing a 19-neuron model using 6 NODs

## [1.0.2] 2024-01-07
### Add
- Working properly distribution process named synapses process. This saves every aspect of the prediction that was carried out, it even will be able to save many predictions done by the same synapses configuration. It's possible to save many synapses, but it was not tested yet. The successful test is in ./nod/test/test_nod_distribution_and_operation.py. It just tests a model of 3 neurons and two NODs. Next tests are going to be considered with bigger models.

## [1.0.1] 2023-12-19
### Add
- Tests for running neurons performing ok.

## [1.0.0] 2023-09-28
### Update
- Orchestration planner working properly according to Test 1, 2, 3 and 4 (./nod/test/test_api_endpoints.py). Test 5, 6 and 7 were partially tested due to many neurons to compare, but visual analysis of the result of the nod distribution looks good. This will test again when running the model.

### Update
- Creacion del repo con las principales partes del mismo para empezar a desarrollar sobre esto. 

