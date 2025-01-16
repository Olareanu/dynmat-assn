# dynmat-assn

A repo for scripts made for the Dynamic behaviour of Materials final Project

| File Name                  | Description                                                                                   |
|----------------------------|-----------------------------------------------------------------------------------------------|
| `abq_full_model.py`        | Script to be run in Abaqus CAE to generate geometry, boundary conditions, job, etc.           |
| `abq_convergence_model.py` | Copy of `abq_full_model.py` but without parameters at the start.                              |
| `convergence_job_gen.py`   | Script to iterate through parameters and create `.inp` files using `abq_convergence_model.py` |
| `job_gen_log.txt`          | Log file with the names of all the generated jobs.                                            |

### Usage of convergence_job_gen.py:
- Set working directory and other parameters in `abq_convergence_model.py`
- Decide what parameters you want to iterate trough and which ones are fixed in `convergence_job_gen.py`
- Run `convergence_job_gen.py` (about 12 seconds per input file generated)
- Check `job_gen_log.txt` to make sure everything was generated, then delete its contents manually
