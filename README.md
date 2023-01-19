# N-Parties Private Parameter and Structure Learning for SPNs
A sum-product network (SPN) is a graphical model that allows several types of inference to be drawn efficiently. This implementation, provides a  privacy-preserving protocol which tackles structure generation and parameter learning of SPNs. To preserve the privacy of the participants, we derive a protocol based on secret sharing, which guarantees privacy in the honest-but-curios setting even when at most half of the parties cooperate to disclose the data. The protocol makes use of a forest of randomly generated SPNs which is trained and weighted privately and can then be used for private inference on data points. Experiments show good log-likelihood performance and the efficiency of the scheme with a varying number of parties on homogeneous and heterogeneous partitioned data. 
## Running on docker
The manger and members of the network can be started with docker. 
* Ensure to install [Docker](https://docs.docker.com/get-docker/) at your machine.
* For running the network locally on your machine create a docker network overlay via 
```
docker network create --driver=overlay --attachable spn_overlay
```

* Use the dockerfiles for manager and member to build docker images 
```
docker build -t manager_build -f dockerfile_manager .
OR
docker build -t member_build  -f dockerfile_member .
```
 

* After building the images they can be run via 
```
docker run --rm --name manager --network spn_overlay --ip 10.0.1.10 -e CONFIG_FILE_LOCATION="./resources/config/config_$dataset_$members_docker.ini" manager_build
OR
docker run --rm --name member$ID --network spn_overlay --ip 10.0.1.1$ID -e CONFIG_FILE_LOCATION="./resources/config/config_$dataset_$members_docker.ini" -e ID_OF_MEMBER="$ID" member_build
```
where $ID is the id of the member you want to run and $dataset the dataset which should be run and $members the number of members in the final network.

* You can close a running docker image with 
```
docker stop manager
OR
docker stop member$ID
```
Additionally, there are some basic docker commands provided in [usefull docker command.txt](usefull%20docker%20commands.txt).


## Reproduce experimental results
The datasets used can be found at https://github.com/arranger1044/DEBD. For bnetflix, baudio, plants, tretail and nltcs the used config files can be found at [resources/config](resources/config). For those datasets the distributed and differently partitioned data is already included in [resources/input](resources/input) for 3, 5 and 10 members, as well as for 3-13 members for the nltcs dataset.

For reproducing the experimental results docker is recommended. 

## Installation and running without docker
For running the protocol on different dataset partitions and with a varying number of members you have to install the following python packages:

```
pip install galois==0.0.20 lark matplotlib nest-asyncio networkx scipy sympy torch tqdm pandas==1.3.1 tensorflow==1.15.0 spflow 
```

Python should be at version 3.7.x as otherwise the tensorflow version does not work.

In the [src](src) folder of the cloned repository you can start the network with `main_$members_$dataset.py` where $members is the number of members in the final network and $dataset the dataset on which the protocol should be performed.
Also, `run.py` or `run_5.py` can be used to start the protocol for all datasets for 3 or 5 members simultaneously. 


## Configuration
For the network to run correct it is important that the IP address of each member is correctly set in all config files.

### General section
In this section are settings, used by all members and the manager.

| name                                                      | type    | meaning                                                                                                                                                                                   |
|-----------------------------------------------------------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| prim_number                                               | Integer | The prime number used to define the ring over intergers for en- and decryption                                                                                                            |
| joint_random_zero_minimum                        | Integer | The minimal value a share of zero can have as additive share                                                                                                                              |
| d_multiplyer                                              | Integer | Used to map real values into integers                                                                                                                                                     |
| sharing_over_integer_max_secret                  | Integer | The greatest allowed value to be encrypted as shares over integers                                                                                                                        |
| sharing_over_integer_allowed_bit_length_of_secret | Integer | The allowed bit-length of a value to be encrypted as shares over integers                                                                                                                 |                                                                                     |
| load_spn_weights                                          | Boolean | If set to true, the network loads the parameters of all SPNs in the forest from the file specified by `spn_weights_file_path` (should be combined with `generate_spn_structures = False)` |
| save_spn_weights                                          | Boolean | If set to true, the network saves the parameters of all SPNs in the forest to the file specified by `spn_weights_file_path`                                                               |
| num_dims                                                  | Integer | Number of dimensions of the dataset                                                                                                                                                       |
| num_local_iterations                                      | Integer | Number of local iterations or stopping criteria for training (20, 30, 40, 100, 300 as number of iterations and 0.001, 0.0005, 0.0001 as stopping criteria are supported)                  |
| ratspn_dictionary                                         | String  | Path to the RAT-SPN dictionary                                                                                                                                                            |
| generate_spn_structures                                   | Boolean | If set to true, a new forest is generated, otherwise the forest from the last run is loaded                                                                                               |
| truncate_n                                                | Integer | Number of Newton iterations                                                                                                                                                               |
| truncate_t                                                | Integer | Precision of the Newton method                                                                                                                                                            |
|private| Boolean | If false, the protocol is performed in a distributed but non-private way                                                                                                                  |
|output_file_path| String  | File were the log-likelihood performance of the protocol is saved, files need to be added when used.                                                                                      |
|sharing_over_integer_security_parameter| Integer | Currently not in use, but left for further improvements                                                                                                                                   |
### ID sections
Each ID section is of pattern `ID_x`, where x should be identical to the ID in the section itself.

| name                  | type    | meaning                                                                                                                                                                    |
| ---                   |---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| id                    | Integer | ID of the member/manager this section is about, used for en- and decryption                                                                                                |
| ip4                   | x.x.x.x | The ip4 adress of this member/manager                                                                                                                                      |
| port                  | Integer | Port used for the communication with the network                                                                                                                           |
| name                  | String  | The name for this member/manager, not used for calculations and comunications                                                                                              |
| latency               | Integer | The delay this member/manager has at sending/receiving a message, with unit milliseconds (ms)                                                                              |
| private_evaluation    | Boolean | If set true, the first x lines of the file specified by `private_data_for_evaluation_file_path` are evaluated, x is specified by `private_evaluation_amount_lines_to_evaluate` |
| private_evaluation_amount_lines_to_evaluate | Integer | The number of lines which should be evaluated of the file specified by `private_data_for_evaluation_file_path`, only invoked when `private_evaluation` is set to True      |
| private_data_file_path | String  | The filepath of the private data used for training the parameters of the RAT-SPN forest                                                                                    |
| spn_file_path         | String  | The filepath of the saved forest, where all SPNs are pickled objects                                                                                                       |
| spn_weights_file_path  | String  | The filepath of the shares this member has on all parameters                                                                                                               |
| private_data_for_evaluation_file_path | String  | The filepath of the private input used for evaluation, which only happens if `private_evaluation` is set to true                                                           |
|saving_checkpoints_file_path | String  | Filepath were checkpoints for the best SPNs are saved                                                                                                                      |
|global_data_for_evaluation_file_path | String  | Filepath were the global data for performance measurement is stored                                                                                                        |

