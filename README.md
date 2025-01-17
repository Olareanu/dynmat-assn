# dynmat-assn

A repo for scripts made for the Dynamic behaviour of Materials final Project

| File Name                  | Description                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `abq_full_model.py`        | Script to be run in Abaqus CAE to generate geometry, boundary conditions, job, etc.            |
| `abq_convergence_model.py` | Copy of `abq_full_model.py` but without parameters at the start.                               |
| `convergence_job_gen.py`   | Script to iterate through parameters and create `.inp` files using `abq_convergence_model.py`. |
| `job_gen_log.txt`          | Log file with the names of all the generated jobs.                                             |
| `euler_job_submission.py`  | Script that loads all the jobs into the queue on euler.                                        |
| `euler_odb_extract.py`     | Script that extracts pictures and CSV files from ODB Databases.                                |
| `euler_plots_from_csv.py`  | Script that generates plots from CSV files on euler.                                           |


### Usage of convergence_job_gen.py:
- Set working directory and other parameters in `abq_convergence_model.py`
- Decide what parameters you want to iterate trough and which ones are fixed in `convergence_job_gen.py`
- Run `convergence_job_gen.py` (about 12 seconds per input file generated)
- Check `job_gen_log.txt` to make sure everything was generated, then delete its contents manually

Useful euler commands and things to know:
```
navigate to cluster/scratch/kurzel
module load abaqus/2023
sbatch -n 4 -t 1-0 --mem-per-cpu 4G --wrap "abaqus job=Job-32 double cpus=4 scratch=\$TMPDIR"
squeue
scancel <job_ID>
scancel --state=PENDING
scontrol show jobid –dd <job_ID>
abaqus cae noGUI=odb_extract.py

```
